# Sources — How Do You Ensure Reliability in an Electrical Equipment Room?

## Tier 1 — standard or code itself

- **NEC 110.26** (working space and access about electrical equipment). Used for: the general
  structure of the clearance rules (clearance scales with voltage and with what's opposite the
  workspace — grounded vs. exposed live parts), the requirement for a dedicated equipment
  space free of unrelated piping/ductwork, headroom, illumination, and entrance/egress sizing
  for large equipment lineups.
  **Accuracy note:** I did not have access to a codebook or the code text itself in this
  session to verify exact table values (the specific foot/inch clearances for each
  voltage/condition combination, exact dedicated-space height, exact ampacity/width threshold
  for the two-entrance requirement). The draft states only the parts of 110.26 that are widely
  and consistently reported at the concept level (clearance scales with voltage and condition;
  ~3 ft baseline at low voltage; dedicated space above equipment; illumination; egress for
  large equipment) and deliberately omits precise numeric table values I could not verify
  directly, per DRAFTING.md's instruction to leave unverifiable specifics out of the body
  rather than assert them. If a reviewer has a current NEC edition on hand, worth a check
  against the exact Table 110.26(A)(1) figures before publish.
- **NFPA 70B** (2023 edition). Used for: the maintenance-program framing (inspection
  intervals, testing methods, documentation) and the "moved from recommended practice to
  enforceable standard in 2023, defines risk-based intervals" claim. This framing is already
  used as an established house fact in the published exemplar ("What is Breaker Testing in
  Electrical Systems.docx" — "NFPA 70B, now an enforceable standard..." / "The 2023 update to
  NFPA 70B reclassified preventive maintenance... as a mandatory requirement"), so it is
  reused here consistently with that precedent rather than re-derived from the standard text.
- **NFPA 70E**. Used for: the general point that arc-flash labeling and risk assessments
  assume the equipment matches the condition described in the coordination study, and that
  drifted trip settings or undocumented load changes undermine that assumption. Stated at a
  conceptual level, no specific article/section cited.
- **NEC Article 517** (health care facilities). Used only for the one-sentence mention that
  hospitals carry additional essential-electrical-system requirements on top of 110.26. Not
  detailed further — flagged as a pointer for anyone drafting a healthcare-specific follow-up,
  not a fully sourced claim in this piece.

## Tier 2 — recognized industry authority

- General practitioner knowledge consistent with how NETA, Mike Holt Enterprises, and ASHE
  commonly describe electrical room clearance and environmental requirements. No single Tier 2
  publication was pulled verbatim; used to sanity-check that the concept-level 110.26
  description above matches how the industry commonly explains it, rather than as a directly
  cited source.

## Tier 3 — trade press / vendor research

- None cited directly. The environmental-control and condition-based-maintenance trend points
  (thermal aging from heat, condensation-driven faults, sensor-based monitoring, digital
  documentation) reflect commonly reported industry practice rather than a single article;
  no vendor product claims are made.

## Numbers deliberately left out of the body

- Exact NEC 110.26 table dimensions by voltage/condition (see accuracy note above).
- Exact dedicated-equipment-space height above switchgear.
- The specific ampacity/width threshold that triggers the two-entrance/egress requirement for
  large equipment (referenced only in general terms — "large switchgear lineups").

None of these omissions affect the article's argument; they were left out rather than guessed,
per DRAFTING.md's accuracy discipline.
