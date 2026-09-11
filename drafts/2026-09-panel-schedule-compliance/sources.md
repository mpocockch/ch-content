# Sources

| Claim | Tier | Source |
|---|---|---|
| Full 408.4(A) circuit directory text: identification wording, "spare" allowance, directory location by equipment type, ban on transient-occupancy descriptions | 1 | NFPA 70 (NEC) 2023 §408.4(A) |
| Arc-flash field label required for equipment likely serviced energized; must show voltage, arc-flash boundary, plus incident energy/working distance or PPE category or minimum arc rating | 1 | NFPA 70E 2024 §130.5(H) (this requirement was §130.5(D) in the 2018 edition; renumbered in the 2021/2024 cycle — confirm edition in use at the facility before citing a section number to a reader) |
| Arc-flash risk assessment reviewed periodically, interval not to exceed 5 years, or sooner on a system change | 1 | NFPA 70E 2024 §130.5(C) |
| NFPA 70B became a mandatory standard (converted from recommended practice) with the 2023 edition; requires a documented Electrical Maintenance Program | 1 | NFPA 70B 2023 edition |
| OSHA control-of-hazardous-energy (lockout/tagout) standard requires isolating and verifying absence of energy before service work | 1 | 29 CFR 1910.147 |
| "It's easier to stay ready than to get ready" framing; original topic pitch | — | Bill Concannon, Teams `Blog Ideas` channel, posted 2026-08-17 |

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
