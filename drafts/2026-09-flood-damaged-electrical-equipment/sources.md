# Sources — Flood-damaged electrical equipment

## Tier 1 — standard, code, or regulator

- **OSHA, Flood Preparedness and Response / Response-Recovery guidance**
  (osha.gov/flood/response) and OSHA disaster-cleanup fact sheets (OSHA FS-3698,
  OSHA 3276). Basis for: de-energize before assessing, do not enter standing water or touch a
  wet panel, do not re-energize equipment that was submerged or sprayed until it has been
  serviced by a manufacturer-approved agency, treat lines/equipment as energized until proven
  otherwise.
- **NFPA 70B, Standard for Electrical Equipment Maintenance.** Basis for the general
  maintenance-testing framework (equipment condition must be verified before it's relied on).
  Used only for that general principle in the draft, since I could not verify flood-specific
  provisions in the 70B text itself from secondary sources alone — nothing flood-specific from
  70B is asserted in the body.

## Tier 2 — recognized industry authority

- **NEMA GD 1-2016 / GD 1-2019, "Evaluating Water-Damaged Electrical Equipment"** (NEMA's
  published guidance; also mirrored by manufacturers including Eaton and referenced by state
  regulators such as Texas TDLR and the National Disaster Recovery response guidance,
  ndresponse.gov). Basis for: the replace-vs-recondition table logic, and specifically that
  panelboard interiors, circuit breakers with electronic trip units, fuse blocks, disconnect
  switches and similar submerged devices should generally be replaced rather than cleaned and
  returned to service, because there is no reliable way to confirm a submerged trip unit will
  still operate correctly.
- **NETA (InterNational Electrical Testing Association) insulation-resistance testing
  practice** (ANSI/NETA MTS reference values; netaworld.org). Basis for: insulation resistance
  ("megger") testing as the core post-flood test, and referencing manufacturer/NETA values
  rather than a pass/fail impression when documenting results. Did not cite a specific numeric
  megohm threshold in the body since that varies by equipment voltage class per NETA's own
  tables — leaving the specific number out per the accuracy-discipline rule rather than
  asserting one value as universal.
- **Megger/AEMC application notes on insulation testing after water/flood damage**
  (aemc.com application note; industry test-instrument vendor guidance). Corroborating,
  non-authoritative source for how insulation resistance testing is applied specifically after
  water exposure.
- **NOAA Climate.gov, "Extreme rainfall brings catastrophic flooding to the Northeast in
  August 2024"** and NOAA/NCICS Connecticut State Climate Summary (statesummaries.ncics.org).
  Basis for the Recent Trends claims: the Connecticut River basin has seen more than double
  the heavy-rainfall events over the past 60 years, Northeast extreme-precipitation frequency
  has grown substantially, and the August 2024 storm near Oxford, CT set record rainfall
  totals NOAA characterized as an approximately 1-in-1,000-year event based on their point
  precipitation frequency estimates. Treated as a government scientific source, cited directly
  rather than paraphrased into a vaguer claim, since the specific figures are attributable to
  a single named NOAA writeup rather than an aggregated web-search synthesis.
- **Transformer oil-testing / dissolved gas analysis (DGA) basics** (Megger and Doble Engineering
  knowledge-hub pages). Basis for citing DGA and dielectric breakdown/moisture-content testing
  as the standard approach for oil-filled transformers, and that water in oil accelerates
  insulation breakdown beyond what a single dielectric reading shows.

## Tier 3 / general corroboration (not cited as the sole basis for any claim)

- Minnesota Department of Labor and Industry, "Flood-damaged electrical systems" and
  "Recommendations for electrical equipment damaged by floodwaters" (dli.mn.gov). Corroborates
  the utility-disconnect and submerged-equipment-replacement points above from a state labor
  regulator's homeowner/contractor guidance rather than a national standard.
- FEMA, "Building Utility Systems: Electrical" fact sheet (fema.gov, Fact Sheet 3.4.2).
  General corroboration for utility-side disconnection practice around flooded service
  equipment.
- Utility company flood-safety pages (e.g., CenterPoint Energy, Hancock-Wood Electric)
  describing that utilities sometimes proactively de-energize service in a flood zone. Used
  only to support "utilities may already be de-energizing proactively, confirm rather than
  assume" language, not as the basis for any specific procedure.

## Left out of the body, deliberately

- No specific NETA minimum insulation-resistance megohm value is stated, since the correct
  value depends on equipment voltage class per NETA's own reference table, and asserting one
  number as universal would be the kind of practitioner-falsifiable claim the drafting
  standard warns against.
- No specific NFPA 70B article or section number is cited, since I could not verify
  flood-specific 70B text directly (nfpa.org itself was not reachable from this environment).
  The 70B reference in the body is limited to the general maintenance-verification principle,
  which is well supported by 70B's stated purpose across multiple secondary sources.
- No claim that any *specific* percentage of flood-damaged equipment fails testing, or that
  any specific dollar figure is typical for flood-related electrical losses. Not verifiable
  from the sources found, so left out entirely rather than estimated.

## Research method note

`nfpa.org` and top-tier trade-press domains were not directly reachable from this environment
(egress-proxy blocked, consistent with prior runs' notes in this repo), so standards-body and
trade-press claims rest on `WebSearch` synthesis of secondary/mirrored sources (state
regulators, manufacturers, testing-instrument vendors, NOAA) rather than a direct primary-text
read. Where a source's own numbers were specific and attributable (NOAA's rainfall figures,
NEMA's replace/recondition guidance as mirrored by multiple independent parties including state
regulators), those were used directly. Where secondary sources only gestured at a standard's
content without quoting it (NFPA 70B's flood-specific provisions, if any), the claim was kept
general rather than asserting specifics that could not be confirmed.
