# Drafting methodology

How a C&H Electric blog post is written. Applies to a new draft (stage 04) and to revisions
(stage 09).

Grounded in two sources, not invented: `C&H Electric Blog Strategy.docx` in the SharePoint Blog
folder, and the published posts in that same folder — `What is Breaker Testing in Electrical
Systems.docx` is the reference exemplar. **When in doubt, open a published post and match it.**

---

## What the blog is for

From the strategy doc, and it governs everything below:

- **Purely informational.** Posts explain complex electrical, safety and compliance topics to
  educate the market and position C&H as a technical authority. They are not promotional.
- **Sales messaging is intentionally limited.** The blog builds trust before selling becomes
  relevant. A post that reads like a brochure has failed.
- **80% evergreen, 20% seasonal.** Most posts should be foundational and valuable all year;
  a fifth respond to news or standards changes.
- Each post is built around **one primary keyword**, and covers that topic with depth and
  practical context rather than surface-level coverage.

---

## Length

**Target 2,000–2,500 words.** The published exemplar is ~2,400. A 1,200-word post on a topic
like this is half-built and will read as thin next to the rest of the blog. Depth is the
strategy — if a draft is coming in short, the cause is usually too few sections, not
short sections. Add the missing angles rather than padding the ones you have.

---

## Metadata block

Every draft opens with this, exactly as the published posts do:

```
Main keyword       breaker testing
URL                breaker-testing
Title              What is Breaker Testing in Commercial Electrical Systems?
Meta description   Learn what is breaker testing and how it impacts functionality and
                   electrical systems of complex facilities.
```

The title usually poses the reader's actual search as a question. The meta description is one
sentence, includes the keyword, and describes what the reader will learn.

---

## Structure

**There is no "Key Takeaways" box.** Earlier versions of this file wrongly required one; the
published posts do not use them. Open instead with:

1. **A hook of one or two sentences that states the stakes concretely.** The exemplar: *"When a
   fault hits, a breaker either does its job or everything else pays for it."* Not a definition,
   not a preamble — the consequence.
2. **A roadmap paragraph** — "This article breaks down what X involves, why it matters, and how
   it differs across…" — so the reader knows the shape of what follows.

Then the body. The recognisable C&H arc, adapted to the topic, is roughly:

| Section | Purpose |
|---|---|
| What is X? | The definition, answered in the first sentence |
| What X involves | The components or sub-activities |
| Why X matters | Consequences of getting it wrong |
| Types / variants | How the work differs by voltage class, facility type, equipment |
| Standards and compliance | NFPA 70B / 70E, OSHA, NETA, IEEE — what each actually requires |
| How often / at what interval | Usually a table |
| Common challenges | The practical obstacles — access, downtime, scheduling, cost |
| Misconceptions | Named false beliefs, each as its own H3, stated then corrected |
| Recent trends | What is changing — new standards, tools, condition-based approaches |
| How to plan / build a program | Numbered steps the reader can act on |
| Final thoughts | Short close. This heading, not "Call to action" |

Not every topic needs all eleven. Most support eight or more, and **Misconceptions** and
**Recent trends** are the two that most often get skipped and shouldn't be — they are where a
post earns its differentiation.

### Section craft

- **Bold the answer sentence** that opens each section. This is a house device and it is visible
  throughout the published posts: the first sentence under a heading answers the heading, and it
  is set in bold. Everything after it elaborates.
- **Use H3 subsections** inside long H2s — voltage classes, individual misconceptions, named
  standards.
- **Use bullet lists** for test types, criteria, checklist items. The published posts use them
  heavily.
- **Use a table** wherever the content is genuinely tabular — intervals, comparisons,
  categories. The exemplar's interval table is the model.

---

## Evidence and citations

Every factual assertion carries a source:

- *Tier 1* — the standard or code itself (NFPA 70B, 70E, NEC), OSHA, IEEE, NETA ATS/MTS.
- *Tier 2* — recognized industry authority (Mike Holt, Brainfiller, ASHE).
- *Tier 3* — trade press (EC&M, Electrical Contractor Magazine) and vendor research.

Prefer Tier 1. Never cite a vendor blog for what a standard says.

**Accuracy discipline.** Verify what a cited standard actually says before asserting it. If
research shows a standard does *not* contain something commonly assumed, say so plainly — the
accurate version is usually the more interesting article, and a claim a practitioner can falsify
destroys the piece's credibility. Arc flash, 70E intervals and 70B requirements are where
received wisdom most often diverges from the text.

If a number cannot be verified, **say so in the sources file and leave it out of the body.**
Do not narrate the refusal to the reader — that is a drafting note, not copy.

---

## Mentioning C&H

The strategy says sales messaging is limited; it does not say C&H is invisible. The published
posts weave the company in as field experience, naturally and in the body:

> "C&H Electric teams often encounter low-voltage breakers left at factory-default settings."

> "Our technicians at C&H Electric are certified to NETA QEMC standards and follow these
> procedures closely."

Two or three such mentions across a post is right. They work because each one carries
information — what C&H sees in the field, what it is certified to — rather than a claim.

---

## Calls to action

**Conditional, not automatic.** Per the strategy: a CTA is used only when the topic directly
intersects a C&H service and the piece has built real intent. When it earns one:

- One mid-article CTA, placed after a section that has just established a risk the reader may
  have (the exemplar puts it after the testing-interval table: *"If you're unsure whether your
  facility meets NFPA 70B maintenance expectations, a simple baseline electrical health audit
  can clarify risk quickly. Contact us today to get started!"*).
- Close on **Final thoughts**, which restates the argument — not a second sales ask.

If the topic does not intersect a service, the post ends on Final thoughts with no CTA at all.
That is a correct outcome, not an omission.

---

## Internal linking

Posts link to other C&H posts to consolidate topic authority, close information gaps and build
progressive learning paths. Mark them `[[internal link: <topic>]]` where one belongs — do not
invent URLs. Aim for three or more per post, placed where a reader would genuinely want to go
deeper, not clustered at the end.

---

## Charts

Include an inline hand-authored SVG chart only if the topic has **3+ genuinely comparable data
points**. Style for a **light background** — absolute colors, not dark-mode-relative. If there is
no comparable numeric series, omit it and say why in the run summary. A table is usually the
better answer for intervals and categories; decoration is not data.

---

## Self-check before handoff

- Word count is 2,000+. If not, name which sections are missing.
- Metadata block present and complete.
- Hook and roadmap paragraph, no Key Takeaways box.
- Each section's opening sentence answers its heading and is bolded.
- Misconceptions and Recent trends sections present, or a reason they don't apply.
- Every claim has a source of a named tier; unverifiable numbers are out of the body.
- CTA is conditional and, if present, mid-article; post closes on Final thoughts.
- 3+ internal link placeholders.
- Banned-phrase check per `VOICE.md`, **excluding your own notes and the word list itself**.

## Output layout

Write to `drafts/<YYYY-MM>-<slug>/`:

```
draft.md          metadata block, then the post
sources.md        every citation with tier and URL
image-brief.md    hero image spec (see IMAGE-BRIEF.md)
hero.jpg          16:9, generated per PLAYBOOK.md §6
```

Commit and push this folder **before** attempting any SharePoint upload.
