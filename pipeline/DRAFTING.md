# Drafting methodology

How a C&H Electric blog post is written. Applies to a new draft (stage 04) and to revisions
(stage 09).

## Structure

1. **Key Takeaways box** at the top — 3–5 bullets a reader can act on without reading further.
2. **Answer-first section openings.** The first sentence under a heading answers the heading.
   No warm-up, no restating the question.
3. **Evidence-backed claims.** Every factual assertion carries a source:
   - *Tier 1* — the standard or code itself (NFPA 70E, 70B, NEC), OSHA, IEEE.
   - *Tier 2* — recognized industry authority (NETA, Mike Holt, Brainfiller, ASHE).
   - *Tier 3* — trade press (EC&M, Electrical Contractor Magazine) and vendor research.
   Prefer Tier 1. Never cite a vendor blog for what a standard says.
4. **Information-gain markers** only where genuinely warranted — a data point, field
   observation or synthesis a reader cannot get from the top-ranking pages. If the section
   adds nothing new, cut it rather than marking it.
5. **Internal-link zone placeholders** — `[[internal link: <topic>]]` where a link to an
   existing C&H page belongs. Do not invent URLs.
6. **A single focused CTA.** One ask, near the end. Not three.
7. **Optional FAQ section** — only for questions real buyers ask, drawn from search intent.
8. **Inline hand-authored SVG chart** if the topic has **3+ genuinely comparable data
   points** worth visualizing. Style for a **light background** — absolute colors, not
   dark-mode-relative ones. If there is no comparable numeric series, omit the chart and say
   why in the run summary. Decoration is not data.

## Accuracy discipline

Verify what a cited standard actually says before asserting it. **If research shows a standard
does not contain something commonly assumed, say so plainly** — the accurate version is
usually the more interesting article, and a claim a practitioner can falsify destroys the
piece's credibility.

Arc flash, 70E intervals and 70B requirements are the areas where received wisdom most often
diverges from the text. Check the text.

## Self-check before handoff

- Run the banned-phrase check in `VOICE.md`. **Exclude your own drafting notes and the word
  list itself from the text being checked**, or the check flags its own vocabulary.
- Every claim has a source of a named tier.
- Exactly one CTA.
- Chart present only if it earned its place; styled for light background.
- Key Takeaways match what the piece actually argues.

## Output layout

Write to `drafts/<YYYY-MM>-<slug>/`:

```
draft.md          front matter: title, slug, target keyword, asana_task, status
sources.md        every citation with tier and URL
image-brief.md    hero image spec (see IMAGE-BRIEF.md)
hero.png          16:9, >=1600px wide — may be added by a human
```

Commit this folder **before** attempting any SharePoint upload.
