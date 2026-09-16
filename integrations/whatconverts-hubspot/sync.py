#!/usr/bin/env python3
"""Sync qualified WhatConverts phone-call leads into HubSpot as Lead records.

For each WhatConverts lead where ``quotable=yes``:

  1. Find (or create) a HubSpot Contact matching the caller's phone number.
  2. Skip if that Contact already has an open Lead -- log a note instead.
  3. Create a Lead in the "New" stage, associated to the Contact.
  4. Attach a note with the call details to the Contact.

State lives entirely in HubSpot: every run re-reads a rolling window and relies
on the two dedup checks to stay idempotent. Missed runs self-heal, and there is
no cursor to corrupt.

The window is 30 days rather than a few hours because ``quotable`` is set by a
human well after the call -- historically a median of ~4.7 days later, up to 18.
The WhatConverts API has no "updated since" filter (``date_type``,
``updated_after`` and ``last_updated`` are all silently ignored), so the only
way to catch a late grading is for the window to still contain the call.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

import requests

LOG = logging.getLogger("wc2hs")

WC_BASE = "https://app.whatconverts.com/api/v1"
HS_BASE = "https://api.hubapi.com"

CONTACT_TYPE = "0-1"
LEAD_TYPE = "0-136"
NOTE_TYPE = "0-46"

NEW_STAGE_ID = "1318266061"

DEFAULT_LOOKBACK_DAYS = 30
WC_PAGE_SIZE = 250

# A caller_name that is carrier CNAM junk rather than a person. WhatConverts
# returns things like "Wireless Caller" or "Hartford     Ct" for most calls;
# using those as a person's name pollutes the CRM.
_CNAM_JUNK = re.compile(
    r"^\s*(wireless caller|toll[\s-]?free|unknown(\s+caller)?|private|"
    r"restricted|anonymous|no name|unavailable|cell ?phone|v[o0]ip)\s*$",
    re.IGNORECASE,
)
# "Hartford     Ct", "Bonita Spg   Fl" -- a place, not a person.
_CNAM_PLACE = re.compile(r"^[A-Za-z.'\- ]+\s{2,}[A-Za-z]{2}\s*$")


class SyncError(RuntimeError):
    """Fatal problem that should stop the run rather than write partial data."""


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

def _request(
    session: requests.Session,
    method: str,
    url: str,
    *,
    max_attempts: int = 5,
    **kwargs: Any,
) -> requests.Response:
    """Issue a request, retrying on 429 and 5xx with exponential backoff."""
    backoff = 1.0
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = session.request(method, url, timeout=30, **kwargs)
        except requests.RequestException as exc:  # connection reset, DNS, TLS
            last_exc = exc
            if attempt == max_attempts:
                raise SyncError(f"{method} {url} failed after {attempt} attempts: {exc}") from exc
            LOG.warning("%s %s: %s -- retry %d/%d", method, url, exc, attempt, max_attempts)
        else:
            if resp.status_code == 429 or resp.status_code >= 500:
                if attempt == max_attempts:
                    raise SyncError(
                        f"{method} {url} returned {resp.status_code} after {attempt} attempts: "
                        f"{resp.text[:400]}"
                    )
                retry_after = resp.headers.get("Retry-After")
                wait = float(retry_after) if retry_after and retry_after.isdigit() else backoff
                LOG.warning(
                    "%s %s -> %s, retrying in %.1fs (%d/%d)",
                    method, url, resp.status_code, wait, attempt, max_attempts,
                )
                time.sleep(wait)
                backoff = min(backoff * 2, 30.0)
                continue
            if not resp.ok:
                raise SyncError(f"{method} {url} -> {resp.status_code}: {resp.text[:400]}")
            return resp
        time.sleep(backoff)
        backoff = min(backoff * 2, 30.0)
    raise SyncError(f"{method} {url} exhausted retries: {last_exc}")


# --------------------------------------------------------------------------
# WhatConverts
# --------------------------------------------------------------------------

class WhatConverts:
    def __init__(self, token: str, secret: str) -> None:
        self._session = requests.Session()
        self._session.auth = (token, secret)

    def qualified_calls(self, start: str, end: str) -> list[dict[str, Any]]:
        """Return quotable phone-call leads created between ``start`` and ``end``.

        The API silently ignores unknown query parameters -- a typo'd filter name
        returns the *entire* unfiltered set rather than an error. Every record is
        therefore re-checked client-side before it can reach HubSpot.
        """
        leads: list[dict[str, Any]] = []
        page = 1
        while True:
            params = {
                "lead_type": "phone_call",
                "quotable": "yes",
                "start_date": start,
                "end_date": end,
                "leads_per_page": WC_PAGE_SIZE,
                "page_number": page,
            }
            payload = _request(self._session, "GET", f"{WC_BASE}/leads", params=params).json()
            batch = payload.get("leads") or []
            leads.extend(batch)
            total_pages = int(payload.get("total_pages") or 1)
            if page >= total_pages or not batch:
                break
            page += 1

        verified = [x for x in leads if str(x.get("quotable", "")).strip().lower() == "yes"]
        if len(verified) != len(leads):
            # The server did not apply the filter we asked for. Rather than sync
            # every call in the window, stop -- something changed API-side.
            raise SyncError(
                f"quotable filter was not applied: {len(leads)} records returned but only "
                f"{len(verified)} are quotable=Yes. Refusing to sync a possibly unfiltered set."
            )
        return verified


# --------------------------------------------------------------------------
# HubSpot
# --------------------------------------------------------------------------

class HubSpot:
    def __init__(self, token: str) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        self._assoc_cache: dict[tuple[str, str], int] = {}

    # -- associations ------------------------------------------------------

    def association_type_id(self, from_type: str, to_type: str) -> int:
        """Look up the default association type id, rather than hardcoding one."""
        key = (from_type, to_type)
        if key in self._assoc_cache:
            return self._assoc_cache[key]
        url = f"{HS_BASE}/crm/v4/associations/{from_type}/{to_type}/labels"
        results = _request(self._session, "GET", url).json().get("results") or []
        if not results:
            raise SyncError(f"no association types between {from_type} and {to_type}")
        # Prefer the unlabeled HubSpot-defined primary association.
        chosen = next(
            (r for r in results if r.get("category") == "HUBSPOT_DEFINED" and not r.get("label")),
            results[0],
        )
        type_id = int(chosen["typeId"])
        self._assoc_cache[key] = type_id
        return type_id

    # -- reads -------------------------------------------------------------

    def leads_by_whatconverts_ids(self, wc_ids: Iterable[str]) -> set[str]:
        """Return the subset of WhatConverts ids that already exist on a Lead."""
        found: set[str] = set()
        ids = [str(i) for i in wc_ids]
        for chunk_start in range(0, len(ids), 100):
            chunk = ids[chunk_start : chunk_start + 100]
            body = {
                "filterGroups": [
                    {"filters": [{
                        "propertyName": "whatconverts_lead_id",
                        "operator": "IN",
                        "values": chunk,
                    }]}
                ],
                "properties": ["whatconverts_lead_id"],
                "limit": 100,
            }
            url = f"{HS_BASE}/crm/v3/objects/{LEAD_TYPE}/search"
            payload = _request(self._session, "POST", url, json=body).json()
            for result in payload.get("results") or []:
                value = (result.get("properties") or {}).get("whatconverts_lead_id")
                if value:
                    found.add(str(value))
        return found

    def find_contact_by_phone(self, e164: str) -> str | None:
        """Find a Contact by phone number. Matching is on phone only, never name."""
        variants = _phone_variants(e164)
        filter_groups = [
            {"filters": [{"propertyName": prop, "operator": "IN", "values": variants}]}
            for prop in ("phone", "mobilephone", "hs_searchable_calculated_phone_number")
        ]
        body = {
            "filterGroups": filter_groups,  # OR'd together
            "properties": ["phone", "mobilephone", "firstname", "lastname"],
            "limit": 5,
            "sorts": [{"propertyName": "createdate", "direction": "ASCENDING"}],
        }
        url = f"{HS_BASE}/crm/v3/objects/contacts/search"
        results = _request(self._session, "POST", url, json=body).json().get("results") or []
        return results[0]["id"] if results else None

    def open_leads_for_contact(self, contact_id: str) -> list[str]:
        """Return ids of Leads on this Contact that sit in an open stage."""
        url = f"{HS_BASE}/crm/v4/objects/contacts/{contact_id}/associations/{LEAD_TYPE}"
        results = _request(self._session, "GET", url, params={"limit": 100}).json().get("results") or []
        lead_ids = [str(r["toObjectId"]) for r in results]
        if not lead_ids:
            return []

        body = {
            "inputs": [{"id": i} for i in lead_ids],
            "properties": ["hs_lead_is_open", "hs_pipeline_stage"],
        }
        read_url = f"{HS_BASE}/crm/v3/objects/{LEAD_TYPE}/batch/read"
        payload = _request(self._session, "POST", read_url, json=body).json()
        open_ids = []
        for result in payload.get("results") or []:
            props = result.get("properties") or {}
            # hs_lead_is_open is "any stage category other than QUALIFIED or
            # UNQUALIFIED" -- more robust than a hardcoded list of stage ids,
            # which would go stale the moment someone adds a stage.
            if str(props.get("hs_lead_is_open")) == "1":
                open_ids.append(str(result.get("id")))
        return open_ids

    def lead_pipeline_id(self) -> str:
        """Resolve the pipeline that owns the New stage, instead of hardcoding it."""
        url = f"{HS_BASE}/crm/v3/pipelines/{LEAD_TYPE}"
        for pipeline in _request(self._session, "GET", url).json().get("results") or []:
            for stage in pipeline.get("stages") or []:
                if str(stage.get("id")) == NEW_STAGE_ID:
                    return str(pipeline["id"])
        raise SyncError(f"no lead pipeline contains stage {NEW_STAGE_ID}")

    # -- writes ------------------------------------------------------------

    def create_contact(self, props: dict[str, str]) -> str:
        url = f"{HS_BASE}/crm/v3/objects/contacts"
        return str(_request(self._session, "POST", url, json={"properties": props}).json()["id"])

    def create_lead(self, props: dict[str, str], contact_id: str) -> str:
        body = {
            "properties": props,
            "associations": [{
                "to": {"id": contact_id},
                "types": [{
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": self.association_type_id(LEAD_TYPE, CONTACT_TYPE),
                }],
            }],
        }
        url = f"{HS_BASE}/crm/v3/objects/{LEAD_TYPE}"
        return str(_request(self._session, "POST", url, json=body).json()["id"])

    def create_note(self, body_html: str, timestamp_ms: int, contact_id: str) -> str:
        body = {
            "properties": {"hs_note_body": body_html, "hs_timestamp": str(timestamp_ms)},
            "associations": [{
                "to": {"id": contact_id},
                "types": [{
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": self.association_type_id(NOTE_TYPE, CONTACT_TYPE),
                }],
            }],
        }
        url = f"{HS_BASE}/crm/v3/objects/notes"
        return str(_request(self._session, "POST", url, json=body).json()["id"])


# --------------------------------------------------------------------------
# Caller name resolution
# --------------------------------------------------------------------------

def looks_like_person(name: str | None) -> bool:
    if not name:
        return False
    name = name.strip()
    if len(name) < 2 or any(ch.isdigit() for ch in name):
        return False
    if _CNAM_JUNK.match(name) or _CNAM_PLACE.match(name):
        return False
    return True


def extract_name_via_claude(lead: dict[str, Any]) -> str | None:
    """Pull the caller's name out of the AI call summary or transcript.

    ``caller_name`` is carrier CNAM data and is a person's name only about a
    third of the time. The summary usually does name the caller, but naming it
    correctly needs judgment a regex does not have: summaries also mention C&H
    staff, the person the caller asked for, and company names, and "speaking in
    Dutch" is not a caller called Dutch.

    Returns None whenever the model is not confident, which falls the caller
    back to the phone number. A missing name is fine; a wrong one is not.
    """
    try:
        import anthropic
        from pydantic import BaseModel
    except ImportError:
        LOG.debug("anthropic/pydantic not installed; skipping name extraction")
        return None

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None

    analysis = lead.get("lead_analysis") or {}
    summary = analysis.get("Lead Summary") if isinstance(analysis, dict) else None
    transcript = lead.get("call_transcription") or ""
    if not summary and not transcript:
        return None

    class CallerName(BaseModel):
        caller_name: str | None
        confident: bool

    source = f"CALL SUMMARY:\n{summary or '(none)'}\n\nTRANSCRIPT:\n{transcript[:6000]}"
    prompt = (
        "This is a record of an inbound phone call to C&H Electric, an electrical "
        "contractor. Identify the name of the PERSON WHO CALLED.\n\n"
        "Set confident=false and caller_name=null unless the caller's own name is "
        "clearly stated. In particular do NOT return:\n"
        "- the name of a C&H Electric employee the caller asked for or left a message for\n"
        "- the name of the person the caller was trying to reach\n"
        "- a company name (return the person's name, not their employer)\n"
        "- a language, city, state, or other non-name word\n\n"
        "Return the caller's own name only, formatted as they would write it.\n\n"
        f"{source}"
    )

    try:
        client = anthropic.Anthropic()
        response = client.messages.parse(
            model="claude-opus-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
            output_format=CallerName,
        )
    except Exception as exc:  # never let name cosmetics fail the sync
        LOG.warning("name extraction failed for lead %s: %s", lead.get("lead_id"), exc)
        return None

    parsed = response.parsed_output
    if parsed and parsed.confident and looks_like_person(parsed.caller_name):
        return (parsed.caller_name or "").strip()
    return None


def resolve_lead_name(lead: dict[str, Any], use_claude: bool) -> str:
    if use_claude:
        extracted = extract_name_via_claude(lead)
        if extracted:
            return extracted
    caller_name = lead.get("caller_name")
    if looks_like_person(caller_name):
        return str(caller_name).strip()
    return str(lead.get("caller_number") or f"WhatConverts lead {lead.get('lead_id')}")


# --------------------------------------------------------------------------
# Mapping
# --------------------------------------------------------------------------

def _phone_variants(e164: str) -> list[str]:
    """Phone spellings to search HubSpot for. Contacts are stored inconsistently."""
    digits = re.sub(r"\D", "", e164 or "")
    variants = {e164, digits}
    if len(digits) == 11 and digits.startswith("1"):
        national = digits[1:]
        variants.update({
            national,
            f"({national[:3]}) {national[3:6]}-{national[6:]}",
            f"{national[:3]}-{national[3:6]}-{national[6:]}",
        })
    return [v for v in variants if v]


def contact_properties(lead: dict[str, Any], display_name: str) -> dict[str, str]:
    props: dict[str, str] = {"phone": str(lead.get("caller_number") or "")}
    if looks_like_person(display_name):
        parts = display_name.split()
        props["firstname"] = parts[0]
        if len(parts) > 1:
            props["lastname"] = " ".join(parts[1:])
    # WhatConverts exposes city/state but no postal code for phone leads.
    if lead.get("city"):
        props["city"] = str(lead["city"])
    if lead.get("state"):
        props["state"] = str(lead["state"])
    return props


def note_body(lead: dict[str, Any]) -> str:
    analysis = lead.get("lead_analysis") or {}
    summary = analysis.get("Lead Summary") if isinstance(analysis, dict) else None
    rows = [
        ("Call date", lead.get("date_created")),
        ("Duration", f"{lead.get('call_duration_seconds')}s"),
        ("Answer status", lead.get("answer_status")),
        ("Tracking number", lead.get("tracking_number")),
        ("Caller ID name", lead.get("caller_name")),
        ("Source / medium", f"{lead.get('lead_source')} / {lead.get('lead_medium')}"),
        ("Campaign", lead.get("lead_campaign")),
        ("Recording", lead.get("recording")),
        ("WhatConverts lead", lead.get("lead_id")),
    ]
    lines = [
        "<p><strong>Inbound call (WhatConverts)</strong></p>",
        "<ul>",
        *[f"<li>{label}: {value}</li>" for label, value in rows if value],
        "</ul>",
    ]
    if summary:
        lines.append(f"<p><strong>Call summary</strong><br>{summary}</p>")
    return "".join(lines)


def _timestamp_ms(iso: str | None) -> int:
    if not iso:
        return int(time.time() * 1000)
    try:
        parsed = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return int(time.time() * 1000)
    return int(parsed.timestamp() * 1000)


# --------------------------------------------------------------------------
# Sync
# --------------------------------------------------------------------------

@dataclass
class Counters:
    fetched: int = 0
    already_synced: int = 0
    leads_created: int = 0
    notes_only: int = 0
    contacts_created: int = 0
    errors: list[str] = field(default_factory=list)


def run_sync(
    wc: WhatConverts,
    hs: HubSpot,
    *,
    lookback_days: int,
    dry_run: bool,
    use_claude: bool,
    only_lead_id: str | None = None,
) -> Counters:
    counters = Counters()
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=lookback_days)

    calls = wc.qualified_calls(start.isoformat(), end.isoformat())
    if only_lead_id:
        calls = [c for c in calls if str(c.get("lead_id")) == str(only_lead_id)]
    counters.fetched = len(calls)
    LOG.info("fetched %d quotable phone-call lead(s) over %d days", len(calls), lookback_days)
    if not calls:
        return counters

    synced = hs.leads_by_whatconverts_ids([c["lead_id"] for c in calls])
    pipeline_id = hs.lead_pipeline_id()

    for call in calls:
        wc_id = str(call.get("lead_id"))
        try:
            if wc_id in synced:
                counters.already_synced += 1
                LOG.debug("lead %s already in HubSpot -- skipping", wc_id)
                continue

            phone = str(call.get("caller_number") or "").strip()
            if not phone:
                counters.errors.append(f"lead {wc_id}: no caller_number")
                continue

            display_name = resolve_lead_name(call, use_claude)

            # (a) Contact: matched on phone only. Matching on caller_name would
            #     collapse every "Wireless Caller" onto a single Contact.
            contact_id = hs.find_contact_by_phone(phone)
            if contact_id is None:
                if dry_run:
                    LOG.info("[dry-run] would create Contact for %s (%s)", phone, display_name)
                    contact_id = "<new>"
                else:
                    contact_id = hs.create_contact(contact_properties(call, display_name))
                    counters.contacts_created += 1
                    LOG.info("created Contact %s for %s", contact_id, phone)

            # (b) Dedup: an open Lead already exists for this caller.
            open_leads = [] if contact_id == "<new>" else hs.open_leads_for_contact(contact_id)

            body = note_body(call)
            stamp = _timestamp_ms(call.get("date_created"))

            if open_leads:
                counters.notes_only += 1
                if dry_run:
                    LOG.info(
                        "[dry-run] lead %s: contact %s has open Lead(s) %s -- would add note only",
                        wc_id, contact_id, ",".join(open_leads),
                    )
                else:
                    hs.create_note(body, stamp, contact_id)
                    LOG.info("lead %s: note added to contact %s (open Lead exists)", wc_id, contact_id)
                continue

            # (c) + (d) Lead, then the call note.
            lead_props = {
                "hs_lead_name": display_name,
                "hs_pipeline": pipeline_id,
                "hs_pipeline_stage": NEW_STAGE_ID,
                "whatconverts_lead_id": wc_id,
            }
            if dry_run:
                LOG.info("[dry-run] would create Lead %r on contact %s", lead_props, contact_id)
                LOG.info("[dry-run] would add note: %s", body[:200])
                counters.leads_created += 1
                continue

            lead_id = hs.create_lead(lead_props, contact_id)
            hs.create_note(body, stamp, contact_id)
            counters.leads_created += 1
            LOG.info("created Lead %s (%s) for WhatConverts %s", lead_id, display_name, wc_id)

        except SyncError as exc:
            # One bad record must not strand the rest of the batch.
            counters.errors.append(f"lead {wc_id}: {exc}")
            LOG.error("lead %s failed: %s", wc_id, exc)

    return counters


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="read only; log intended writes")
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=int(os.environ.get("LOOKBACK_DAYS", DEFAULT_LOOKBACK_DAYS)),
    )
    parser.add_argument("--lead-id", help="process a single WhatConverts lead id")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
    )

    missing = [k for k in ("WC_TOKEN", "WC_SECRET", "HUBSPOT_TOKEN") if not os.environ.get(k)]
    if missing:
        LOG.error("missing required environment variable(s): %s", ", ".join(missing))
        return 2

    use_claude = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if not use_claude:
        LOG.info("ANTHROPIC_API_KEY not set -- falling back to caller_name heuristics")

    wc = WhatConverts(os.environ["WC_TOKEN"], os.environ["WC_SECRET"])
    hs = HubSpot(os.environ["HUBSPOT_TOKEN"])

    try:
        counters = run_sync(
            wc, hs,
            lookback_days=args.lookback_days,
            dry_run=args.dry_run,
            use_claude=use_claude,
            only_lead_id=args.lead_id,
        )
    except SyncError as exc:
        LOG.error("run aborted: %s", exc)
        return 1

    LOG.info(
        "done: fetched=%d already_synced=%d leads_created=%d notes_only=%d "
        "contacts_created=%d errors=%d",
        counters.fetched, counters.already_synced, counters.leads_created,
        counters.notes_only, counters.contacts_created, len(counters.errors),
    )
    for err in counters.errors:
        LOG.error("  %s", err)
    return 1 if counters.errors else 0


if __name__ == "__main__":
    sys.exit(main())
