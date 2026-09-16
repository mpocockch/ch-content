# HubSpot CRM conventions — C&H Electric

Rules for anything that writes to HubSpot portal **48530303**, and the portal behaviour
worth not re-deriving. Written after building the WhatConverts lead sync
(`integrations/whatconverts-hubspot/`), where several of these were learned the hard way.

Read this before writing to the portal. Several rules exist because a previous session
did the reasonable-looking thing and it was wrong.

## Naming

- **A Lead is named after the person, never the company.** `hs_lead_name` is documented as
  "the full name of the lead", and HubSpot carries company identity separately through the
  company association and `hs_associated_company_name`, which can be its own column in the
  Leads list view. Putting the company in the name duplicates a field that already exists.
- **No project or scope text in a name field.** "Huff Energy Solutions – Milford, CT BESS
  Install" was a Lead name here once. It reads well on one row and badly on a hundred: it
  cannot be sorted, is unreliable to search, and a second project for the same account
  produces two Leads whose names differ by a substring.
- **Never use carrier caller-ID (CNAM) as a person's name.** Over 90 days of calls, 47 of
  279 read "Wireless Caller", 87 more were `City ST` strings, and when it did look like a
  name it could be the account holder rather than the caller — one call reads "Mario
  Malangone" for a caller both the transcript and the matching CRM contact identify as
  Dana. A blank name prompts someone to look; a plausible wrong one gets trusted.
- **Take the name from the matched contact, and set it explicitly.** When a phone number
  matches a contact that already has a name, that is the name C&H recorded for that number
  and is the best source available. Write it at creation: left empty, HubSpot fills the
  field in itself about 8 seconds later as `<contact name> <YYYY-MM>`, and nobody wants a
  date in a name field. A name written at creation is not touched.
- **Blank beats wrong.** With no trustworthy source, leave the name empty rather than
  guess it.

## Attribution

- **Never overwrite a contact's Original Traffic Source** (`hs_analytics_source`), with one
  exception: `OFFLINE`, which is what HubSpot records for anything typed into the CRM by
  hand and carries no real attribution. "Original" means first touch; a later interaction
  does not get to rewrite it.
- **Google Business Profile calls (`gmb` / `organic`) count as Organic Search.** This is
  the single largest bucket — 182 of 279 calls over 90 days — so anyone reading Organic
  Search as a measure of SEO performance should know that GBP click-to-call is inside it.

## Ownership

- **Synced records are created unowned.** `hubspot_owner_id` is left unset so Leads land
  unassigned for triage rather than being routed automatically.

## Filling in blank Lead names

Leads arriving from an automated source can have no name. Who completes them, and how
quickly, is a C&H team process — not something an integration decides. Anything automated
should leave the field empty rather than invent a value.

## Portal behaviour, verified

Facts established against the live portal. They cost real debugging; do not assume
otherwise without re-testing.

| Behaviour | Detail |
| --- | --- |
| Lead pipeline and stage ids are **strings** | `hs_pipeline` is `lead-pipeline-id`, `hs_pipeline_stage` is `new-stage-id`. Numeric ids that appear inside property *names* (e.g. `hs_v2_date_exited_new_stage_id_1318266061`) are something else and are not valid stage values. Resolve stages from `/crm/v3/pipelines/0-136` by label. |
| `hs_lead_name` is backfilled **asynchronously** | About 8 seconds after creation, as `<contact name> <YYYY-MM>` — but only when the associated contact has a name, and only when the field was left empty. A name supplied at creation is left alone. With a nameless contact the field stays empty. Reading a Lead back immediately after the POST shows `null` even when a name is coming. |
| Lead → Contact has **two** association types | `578` "Primary" makes the contact the lead's primary contact; `608` is unlabeled and does not. Prefer Primary. |
| `hs_lead_source` on a Lead is always `OFFLINE` via the API | HubSpot assigns Offline Sources to anything created through the API, regardless of the contact's analytics source and whenever it was set. It is not settable. Attribution lives on the contact. |
| A Lead **requires** an association | To a Contact or Company, supplied at creation. |
| Search is **eventually consistent** | A deleted record can still be counted in `total` for a short time while returning no rows. Verify a delete with a direct `GET` (404), not a search. |

## Matching

- **Match contacts on phone number, never on name.** Names from external sources collide —
  matching on CNAM would have collapsed 47 unrelated callers onto a single contact.
