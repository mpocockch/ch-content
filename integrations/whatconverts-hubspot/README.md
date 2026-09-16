# WhatConverts -> HubSpot lead sync

Creates a HubSpot **Lead** (plus Contact and call note) for every WhatConverts
phone call a rep has marked `quotable = Yes`. Replaces the Zapier integration.

## How it runs

`.github/workflows/whatconverts-hubspot-sync.yml` runs `sync.py` every 30
minutes, 11:00-23:30 UTC, Mon-Fri -- 07:00-19:30 Eastern in summer. You can
also run it by hand from the Actions tab ("Run workflow"), which defaults to a
dry run.

**Scheduled runs are dry by default.** They write to HubSpot only once the
repository variable `DRY_RUN` is explicitly set to `false`. Any other value --
unset, `true`, `False`, junk -- leaves the job in dry-run mode. Merging the
workflow therefore cannot by itself start writing to the production portal.

### Going live

1. Merge to the default branch. Scheduled runs begin, but stay dry.
2. Actions tab -> this workflow -> **Run workflow**, leave dry-run ticked.
   Read the log and confirm the records it *would* create look right.
3. Settings -> Secrets and variables -> Actions -> **Variables** ->
   `DRY_RUN` = `false`.
4. To pause writes again, set `DRY_RUN` back to `true`. No code change, no
   redeploy.

## Setup

### 1. HubSpot private app

Settings -> Integrations -> Private apps -> Create. Grant read **and** write on
Contacts, Leads, and Notes (the scopes are named `crm.objects.contacts.*`,
`crm.objects.leads.*` and `crm.objects.notes.*`; tick the matching boxes in the
UI rather than typing them). Copy the access token.

### 2. Repository secrets

Settings -> Secrets and variables -> Actions:

| Secret | Value |
| --- | --- |
| `WHATCONVERTS_TOKEN` | WhatConverts API token (profile 172135) |
| `WHATCONVERTS_SECRET` | WhatConverts API secret |
| `HUBSPOT_PRIVATE_APP_TOKEN` | Token from step 1 |
| `ANTHROPIC_API_KEY` | Optional -- enables caller-name extraction |

And under the **Variables** tab (not Secrets):

| Variable | Value |
| --- | --- |
| `DRY_RUN` | `false` to let scheduled runs write. Omit it until you have read a dry-run log. |

### 3. Custom property

`whatconverts_lead_id` (single-line text) on the **Lead** object. Already
created in portal 48530303; a fresh portal needs it before the first run.

## Running locally

```bash
pip install -r requirements.txt
export WC_TOKEN=... WC_SECRET=... HUBSPOT_TOKEN=...
python sync.py --dry-run                 # read-only, logs intended writes
python sync.py --lead-id 258203524       # single record
python sync.py                           # live
```

## What it does per call

1. **Contact** -- matched on `caller_number` only, created if absent.
2. **Dedup** -- if that Contact already has a Lead in an open stage, no second
   Lead is created; the call is attached as a note instead.
3. **Lead** -- `hs_pipeline_stage = 1318266061` ("New"), `whatconverts_lead_id`
   set for dedup on later runs.
4. **Note** -- call metadata plus the AI call summary, on the Contact.

## Design notes

**30-day window, no stored cursor.** Each run re-reads 30 days and relies on two
dedup checks to stay idempotent, so a missed run self-heals. The window is 30
days rather than hours because `quotable` is set by a human long after the call
-- historically a median of ~4.7 days, up to 18. The WhatConverts API has no
"updated since" filter (`date_type`, `updated_after` and `last_updated` are all
silently ignored), so a short window would close before a rep grades the call.
Cost is one request per run against a 10,000/day limit.

**The `quotable` filter is re-checked client-side.** WhatConverts silently
ignores unknown query parameters: `quotabel=yes` returns all 279 records rather
than erroring. A typo would otherwise sync every call in the window into
production. `qualified_calls()` aborts the run if any returned record is not
`quotable=Yes`.

**Contacts are matched on phone, never on name.** `caller_name` is carrier CNAM
data -- 47 of 279 recent records are literally "Wireless Caller" and another 87
are `City ST` strings. Matching on it would collapse dozens of unrelated callers
onto one Contact.

**Lead names come from the call summary when possible.** `caller_name` is a real
person's name only about half the time, and even then it can be the account
holder rather than the caller (one record's CNAM says "Mario Malangone" while
the summary says "Dana from Malangorn Electric called"). With `ANTHROPIC_API_KEY`
set, the summary and transcript are read to identify the caller, returning
nothing unless confident -- summaries also name C&H staff, the person the caller
asked for, and companies. Without the key it falls back to a `caller_name`
heuristic, then the phone number. An extracted name is display text only; it
never affects Contact matching, so a bad extraction is cosmetic.

**Open-lead detection uses `hs_lead_is_open`** rather than a hardcoded list of
open stage ids, so adding a pipeline stage doesn't silently break dedup.

**Pipeline and association type ids are resolved at runtime** from the HubSpot
API instead of hardcoded, since only the stage ids were known up front.
