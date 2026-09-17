# Sources

| Claim | Tier | Source |
|---|---|---|
| Full 408.4(A) circuit directory text: identification wording, "spare" allowance, directory location by equipment type, ban on transient-occupancy descriptions | 1 | NFPA 70 (NEC) 2023 §408.4(A) |
| OSHA control-of-hazardous-energy (lockout/tagout) standard requires isolating and verifying absence of energy before service work | 1 | 29 CFR 1910.147 |
| "It's easier to stay ready than to get ready" framing; original topic pitch | — | Bill Concannon, Teams `Blog Ideas` channel, posted 2026-08-17 |

## Revision note, 2026-09-17

A reviewer edited the Word doc directly in SharePoint (no Asana comment) sometime before
2026-09-16T13:36 UTC, dropping the entire NFPA 70E arc-flash-label / NFPA 70B EMP framing from
"What Panel Schedule Compliance Involves," "Standards and Compliance," "Misconceptions," "Recent
Trends" and the how-to-build list, and replacing it with a legibility/digitization framing
(handwritten directories, phone/tablet/desktop updates, who can make a field change). This run
implemented that direction in `draft.md`, matching the reviewer's wording to house structure
(bold lead sentences, heading hierarchy). Removed the 70E 130.5(H)/(C) and 70B 2023 citations
below accordingly, since neither standard is asserted in the body anymore. If a future revision
wants the arc-flash-label angle back, the citations were:
- NFPA 70E 2024 §130.5(H) — arc-flash field label required for equipment likely serviced
  energized (renumbered from §130.5(D) in the 2018 edition).
- NFPA 70E 2024 §130.5(C) — arc-flash risk assessment reviewed periodically, interval not to
  exceed 5 years, or sooner on a system change.
- NFPA 70B 2023 edition — became a mandatory standard (from a recommended practice), requires a
  documented Electrical Maintenance Program.

## Verification notes

- **408.4(A) citation, corrected this revision.** The prior draft quoted 408.4(A) with an
  ellipsis that cut off the sentence establishing directory location, then separately asserted
  the location rule (face of panel / inside door / at each breaker for switchgear) as if it
  followed from the quoted text — it didn't, and an editor correctly flagged this as an
  unsupported claim riding on a truncated quote. This revision uses the full, untruncated
  sentence, so the location claim is now directly inside the quote rather than adjacent to it.
  The exact wording ("located on the face, inside, or in an approved location adjacent to the
  panel door... and at each switch or circuit breaker in a switchboard or switchgear") was
  cross-checked across several independent secondary sources describing the current-edition
  text — Mike Holt Enterprises' code forums, EC&M's code-analysis coverage, and Leviton's
  Captain Code NEC portal — which converge on identical wording. That's multiple independent
  Tier 2/3 sources agreeing, not a single secondary source repeated; it is still not a
  from-the-purchased-code-book verification, and that limitation should be corrected the next
  time someone on the team has the actual 2023 NEC volume in hand.
- 70E 130.5(H)/(C) content confirmed via multiple secondary sources describing current-edition
  numbering; the section letter has moved between editions (130.5(D) → 130.5(H) for the label
  requirement), so the draft names both the requirement and this renumbering rather than
  asserting one letter as permanent.
- **No numeric cost comparison** (incremental labeling vs. full facility retrace) is cited
  because none could be verified from a Tier 1–3 source in this run. The prior draft narrated
  this refusal directly to the reader in a paragraph starting "We're not aware of a published
  industry figure..." — an editor correctly flagged that as drafting-process commentary that
  had leaked into the reader's copy. This revision removes that paragraph entirely from
  draft.md; the honest gap is recorded here instead, and the body simply describes the shape of
  the cost (labor to trace circuits, coordination overhead, shutdown scheduling) without
  attaching an unverified number to it.
- The lockout/tagout and emergency-response scenarios in "The Safety Case" section are
  illustrative, grounded in what 29 CFR 1910.147 actually requires (isolate, then verify absence
  of energy) rather than a cited incident — no specific injury or event is claimed, only the
  mechanism by which a wrong directory undermines that sequence.
