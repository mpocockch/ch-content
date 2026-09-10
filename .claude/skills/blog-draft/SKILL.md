---
name: blog-draft
description: Write or revise a C&H Electric blog post following the house SEO and voice methodology. Use when drafting a new post from an approved Asana topic, implementing reviewer edits on a draft in Waiting Approval, or whenever writing content destined for chelectric.com. Loads the drafting structure, source-tier rules, banned-phrase list and output layout.
---

# Blog draft

Write or revise a C&H Electric blog post.

## Before writing

1. Read `pipeline/DRAFTING.md` — structure, source tiers, accuracy discipline, output layout.
2. Read `pipeline/VOICE.md` — tone and the banned-phrase list.
3. Read `pipeline/PLAYBOOK.md` §3 for the Asana IDs, and §5 for failure handling.
4. Check `drafts/` for an existing folder for this topic. **If one exists, resume it** — do
   not start over, and do not regenerate an image or rewrite a section a prior run finished.

## Writing

Follow `DRAFTING.md` exactly: Key Takeaways box, answer-first openings, tiered citations,
internal-link placeholders, one CTA, optional FAQ, and an SVG chart only if the topic has 3+
genuinely comparable data points.

Verify what standards actually say before asserting it. A claim a practitioner can falsify
destroys the piece.

## Revising

When implementing reviewer edits, work from the reviewer's actual words — the Asana comment or
the Word doc markup. Ambiguous feedback gets a clarifying reply on the card, not a guess.
Treat a direct question from Matt or Bill as work to be done: answer it in a reply comment
before drafting, since their input often decides the angle or the target keyword.

## Finishing

1. Run the self-check in `DRAFTING.md` — **excluding your own notes and the banned-phrase list
   itself** from the text being checked.
2. Write `draft.md`, `sources.md` and `image-brief.md` into `drafts/<YYYY-MM>-<slug>/`.
3. **Commit.** Before any upload attempt.
4. Append to `pipeline/STATE.md`.
