---
name: blog-draft
description: Write or revise a C&H Electric blog post following the house SEO and voice methodology. Use when drafting a new post from an approved Asana topic, implementing reviewer edits on a draft in Waiting Approval, or whenever writing content destined for chelectric.com. Loads the drafting structure, source-tier rules, banned-phrase list and output layout.
---

# Blog draft

Write or revise a C&H Electric blog post.

## Before writing

1. Read `pipeline/DRAFTING.md` in full — it is the house standard and it is specific. Length
   target, metadata block, section architecture, bolded answer sentences, conditional CTA.
2. Read `pipeline/VOICE.md` — tone and the banned-phrase list.
3. **Read a published post before drafting.** `What is Breaker Testing in Electrical
   Systems.docx` in the SharePoint Blog folder is the reference exemplar. Matching the real
   thing beats following a description of it, and the folder holds a dozen more.
4. Read `pipeline/PLAYBOOK.md` §3 for the Asana and SharePoint IDs, and §5 for failure handling.
5. Check `drafts/` for an existing folder for this topic. **If one exists, resume it** — do
   not start over, and do not regenerate an image or rewrite a section a prior run finished.

## Writing

Follow `DRAFTING.md` exactly. The things most often got wrong:

- **2,000–2,500 words.** Short drafts are the commonest defect. If you are coming in under,
  you are missing sections, not sentences.
- **No Key Takeaways box.** Open with a stakes hook, then a roadmap paragraph.
- **Bold the answer sentence** that opens each section.
- **Include Misconceptions and Recent trends** — the two sections that most differentiate a
  C&H post and the two most often skipped.
- **CTA only if the topic intersects a C&H service**, placed mid-article, and close on
  Final thoughts.

Verify what standards actually say before asserting it. A claim a practitioner can falsify
destroys the piece. If a figure cannot be verified, leave it out of the body and note why in
`sources.md` — do not narrate the omission to the reader.

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
