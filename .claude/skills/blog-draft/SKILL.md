---
name: blog-draft
description: Write or revise a C&H Electric blog post, plus the LinkedIn post that links out to it, following the house SEO and voice methodology. Use when drafting a new post from an approved Asana topic, implementing reviewer edits on a draft in Waiting Approval, or whenever writing content destined for chelectric.com. Loads the drafting structure, source-tier rules, banned-phrase list, LinkedIn post standard and output layout.
---

# Blog draft

Write or revise a C&H Electric blog post.

## Before writing

1. Read `pipeline/DRAFTING.md` in full — it is the house standard and it is specific. Length
   target, metadata block, section architecture, bolded answer sentences, conditional CTA.
2. Read `pipeline/VOICE.md` — tone and the banned-phrase list. Read `pipeline/LINKEDIN.md`
   too: every draft ships with a LinkedIn post, and it has its own structure and length.
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
- **Never credit or describe an internal comment, pitch, or review note in the copy** — not
  Matt's, not Bill's, not the original Teams idea post's, even in passing ("Bill's framing from
  the pitch holds up well"). The reader was never shown that context and it reads as an editing
  artifact. If the underlying idea is good, use it in the article's own voice with no internal
  attribution. See `DRAFTING.md`'s "Never narrate the review process" section for the real
  defect this rule was written to stop.

Verify what standards actually say before asserting it. A claim a practitioner can falsify
destroys the piece. If a figure cannot be verified, leave it out of the body and note why in
`sources.md` — do not narrate the omission to the reader.

## Revising

When implementing reviewer edits, work from the reviewer's actual words — the Asana comment or
the Word doc markup. Ambiguous feedback gets a clarifying reply on the card, not a guess.
Treat a direct question from Matt or Bill as work to be done: answer it in a reply comment
before drafting, since their input often decides the angle or the target keyword.

Pull the substance of a review comment or idea-post note into the piece, never the fact that it
was said in review. "Bill wants more on the safety angle" becomes a safety section — it does
not become a sentence telling the reader that Bill wanted more on the safety angle.

## The LinkedIn post

**Every blog draft gets one — no exceptions, same run, not a follow-up task.** It links out to
the article and is what actually drives traffic to it.

Follow `pipeline/LINKEDIN.md`: 120–250 words, a one-line hook, short paragraphs with real white
space, an arrow (`→`) list of three to five specifics pulled from the article, one standard or
code anchor, and a link close using the phrasings already in use. No hashtags, no markdown
formatting (LinkedIn renders none of it), no second CTA stacked on the link.

Tease the article, don't summarize it — a post that delivers the whole argument removes the
reason to click. Build the URL from the draft's metadata `URL` field and flag it as provisional
until the article is live.

Write it to `drafts/<YYYY-MM>-<slug>/linkedin.md`, post body first and pasteable as-is, notes
below a `---` separator.

## Finishing

1. Run the self-check in `DRAFTING.md` — **excluding your own notes and the banned-phrase list
   itself** from the text being checked.
2. Write `draft.md`, `sources.md`, `image-brief.md` and `linkedin.md` into
   `drafts/<YYYY-MM>-<slug>/`.
3. **Commit.** Before any upload attempt.
4. Append to `pipeline/STATE.md`.

Carry the LinkedIn post through the handoff with everything else: append it to the end of the
Word doc under a `LinkedIn post` heading so reviewers see it on the same review surface, include
`linkedin.md` in the `SendUserFile` delivery, and say it's there in the Asana comment. It adds
well under a kilobyte to the `.docx`, but PLAYBOOK.md §4's ~18 KB upload ceiling still governs —
shrink the embedded hero preview, never the copy.
