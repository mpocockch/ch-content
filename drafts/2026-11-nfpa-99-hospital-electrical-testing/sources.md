# Sources: "What Electrical Testing Does NFPA 99 Require in Hospitals?"

Research note: in the 2026-11-17 run, WebFetch could not resolve any external host (eaton.com,
jointcommission.org, facilitiesdive.com, the CFE Media e-edition all returned ENOTFOUND from the
session's network policy). Every claim below was checked through web search result extracts
only, not by reading the source page in full. Reviewers with an NFPA 99 copy should spot-check
the starred items against the text.

## Tier 1 (standards, regulators, accreditors)

- **NFPA 99, Health Care Facilities Code** (2012, 2021, 2024 editions).
  https://www.nfpa.org/product/nfpa-99-health-care-facilities-code/p0099code
  - Risk categories 1–4 and EES Type 1 / Type 2 requirements by category (Ch. 4, Ch. 6).
  - * LIM test by actuating the test switch at intervals of not more than 1 month; not more than
    12 months for LIMs with automated self-test and self-calibration. Verified wording found only
    in a reproduced 1999-edition excerpt (ssr-cfm-articles.blogspot.com, 2011) and vendor
    guidance (Schneider Electric FAQ FA177587, Bender LT3000 datasheet); the Mike Holt forum
    places it at 6.3.3.3.2 in newer editions. Check against the 2012 text.
  - Receptacle tests: physical integrity, grounding continuity, polarity, retention force not
    less than 115 g (4 oz) for non-locking receptacles; hospital-grade at bed locations tested
    after installation/replacement/servicing, then at intervals from documented performance
    data. Sources: IAEI Magazine "Receptacle Testing in Patient Care Areas"; Missouri DHSS
    "Electrical Receptacle Testing"; HFM Magazine "Receptacle testing in patient areas".
  - * 2021 edition s6.9: all components serving Category 1 or 2 spaces in an electrical
    maintenance program complying with NFPA 70B s4.2; Table 6.9.4.1 intervals, 3 years for
    LV power and molded-case breakers; annex Table A.6.9.4.1 points to NFPA 70B. Sources: NFPA
    committee minutes 99A2026CYCLE_HEA-ELS_SDMinutes_08_25.pdf (docinfofiles.nfpa.org); CSE
    Magazine Spring 2022 (CFE Media); Eaton white paper WP083045 "Addressing 2021 NFPA 99
    updates".
- **NFPA 110, Standard for Emergency and Standby Power Systems** (2010 edition, as enforced).
  - Weekly inspection; monthly 30-min load run at >=30% nameplate kW or manufacturer's minimum
    exhaust temperature; annual supplemental load 50% x 30 min + 75% x 60 min (1.5 h) when
    monthly tests fall short; 4-hour run every 36 months; monthly transfer switch operation;
    EPSS breakers exercised annually; breakers over 600V exercised every 6 months and tested
    under simulated overload every 2 years (8.4.x). Sources: Minnesota Dept. of Health
    lscgensets24.pdf; Joint Commission FAQ 000001267; HFM Magazine "Emergency power code
    revisions". The breaker rows (8.4.7, 8.4.8) were not seen in a search extract; they are
    from the drafter's knowledge of NFPA 110-2010 and are starred for checking. *
- **Joint Commission EC.02.05.07** and FAQ "Emergency Generator 4-hour Load Test":
  4-hour test at least every 36 months, 30% nameplate for diesel; monthly tests 20–40 days
  apart. https://www.jointcommission.org/standards/standard-faqs/home-care/environment-of-care-ec/000001267
- **CMS final rule, 81 FR 26871 (May 4, 2016)**, adopting the 2012 LSC and 2012 NFPA 99.
  https://www.federalregister.gov/documents/2016/05/04/2016-10043/medicare-and-medicaid-programs-fire-safety-requirements-for-certain-health-care-facilities
- **CMS QSO-23-11-LSC (March 31, 2023)**, categorical waiver for health care microgrid systems,
  conditioned on NFPA 99-2021 and NFPA 70-2023; must be elected and documented before survey.
  https://www.cms.gov/files/document/qso-23-11-lsc.pdf
- **NFPA 70B** became a Standard (from Recommended Practice) effective with the 2023 edition.
  https://en.wikipedia.org/wiki/NFPA_70B (Tier 3 pointer; the fact is from NFPA itself.)

## Tier 2 / 3

- NIH ORF Technical Bulletin, "Electrical Design of Healthcare Facilities," Feb 2026 (Category
  1 -> Type 1; Category 2 -> Type 1 or 2; Category 3 no EES; branch structure).
  https://orf.od.nih.gov/TechnicalResources/Documents/Technical%20Bulletins/26TB/Electrical%20Design%20of%20Healthcare%20Facilities%20-%20February%202026%20TB_508.pdf
- Facilities Dive, "Experts detail 2027 updates to NFPA Health Care Facilities Code" (ASHE 2026
  coverage): Chapter 6 risk-mitigation design language, isolated power / telecom room spacing,
  new Chapter 17 cybersecurity.
  https://www.facilitiesdive.com/news/experts-detail-2027-updates-to-nfpa-health-care-facilities-code/827561/
- PG LifeLink isolated power testing; MGI EPSS generator requirements (from the Asana card;
  vendor sources, used only as pointers, not cited for what a standard says).

## Deliberately left out of the body

- **"NFPA 99 2027 edition is now published"** (claim on the Asana card). Could not confirm an
  issue date. Search found second-draft ballots (late 2025) and a TIA log referring to the
  "proposed 2027 edition" with comments closing May 22, 2026. The body says the 2027 edition is
  "working its way through NFPA's process". Update if NFPA has issued it.
- **A 12-month maximum interval for non-hospital-grade receptacles.** Believed to be in the 2012
  text but not confirmed by any search extract. Left out.
- **A 5-year record-retention period.** One CMS document extract tied this to NFPA 99-2021 s6.9,
  but the context was unclear. Left out.
- **NFPA 70B condition-based interval numbers.** Not needed for the argument; avoided to keep
  the body free of figures we did not verify for this post.
