# LinkedIn posts

Every blog draft ships with a LinkedIn post that links out to the article. Written at stage 04
alongside the draft, reviewed with it, posted when the article goes live.

Grounded in the real thing, not invented: **`Company LinkedIn posts.docx`** in the SharePoint
Marketing folder, which holds the posts C&H has actually published. Read it before writing.

- driveId: `b!rFOk2NgZLUanLuEhSAQO6XVd1ws0aSJIhZeZ6Guiew2nCeXLAPUoQ41jyCucuNy_` (same drive as
  the Blog folder, `PLAYBOOK.md` §3)
- folder: `SERVICE/SERVICE OFFICE/6. Marketing/LinkedIn posts`
- item: `01W45A5ET4WDSZWPZD5RC3QIHUXLN3DSFQ`

`Bill's LinkedIn Prompts.docx` sits in the same folder. It is an interview prompt list for
Bill's *personal* profile — not the company voice, and not the standard for this. Don't use it.

---

## Shape of a blog-linked post

Five moves, in this order. The published posts follow it closely.

1. **A hook on its own line.** One sentence, no preamble. The patterns that recur:
   - *The correction* — "Most facilities don't know which OSHA standard governs them."
   - *Their facility, specifically* — "Your electrical panel could be hiding something from
     you." / "Your AIC rating is wrong. You just don't know it yet."
   - *The flat statement* — "A circuit breaker has one job." / "The NEC isn't just for
     electricians."
   - *The question* — "What's the most expensive thing in your facility?"
2. **Two to four short paragraphs**, one idea each, blank line between. One to three sentences
   per paragraph. White space is the format — a dense block reads as an article, not a post.
3. **An arrow list of three to five concrete specifics** — symptoms, findings, requirements,
   consequences. `→` is the house bullet and the most recognizable device in these posts. `❌`
   works for a list of what a facility is missing.
4. **One standard or code anchor**, stated plainly: what NFPA 70B, 70E, the NEC or OSHA
   actually requires or changed. One is enough; this is the credibility beat, not a summary.
5. **The link close.** Name what the article covers in a sentence, then the URL. Use the
   phrasings already in use rather than inventing new ones:
   - "We've published an in-depth article on <topic> that you can read here: <URL>"
   - "We put together a guide explaining <what>. Read our detailed guide on the topic here:
     <URL>"
   - "We broke down <what>. Read the full guide here: <URL>"

**Length: 120–250 words.** The published blog-linked posts run 130–200.

### The URL

Build it from the `URL` field in the draft's metadata block: `https://chelectric.com/<url>/`.
It is provisional until the post is actually live — stage 11 records the real URL, and the
LinkedIn post's link gets reconciled against it before anyone posts. Say so in the notes
section of `linkedin.md`; never present an unpublished link as live.

---

## Voice

`VOICE.md` applies in full — same banned phrases, same second person, same refusal to sound
like marketing. On top of it:

- **Shorter sentences than the blog.** One idea per line. Cut every clause that isn't load
  bearing.
- **No hashtags.** The published technical and blog-linked posts don't use them. (They appear
  only on people and celebration posts, which is a different format.)
- **Emoji are structural, never decorative.** `→` for list items, `❌` for what's missing, `👇`
  only when pointing at the link. Nothing else.
- **Tease, don't summarize.** Three to five concrete specifics from the article, then the
  link. A post that delivers the whole argument removes the reason to click.
- **Never invent a number.** Same accuracy discipline as `DRAFTING.md` — every claim traces
  back to the draft, which traces back to `sources.md`.
- **Never reference internal comments, pitches, or review notes** — same rule as the blog copy
  (`DRAFTING.md`, "Never narrate the review process in the copy").
- **One close, not two.** A blog-linked post closes on the link. Don't stack a "reach out to
  C&H Electric" ask on top of it; the service-led posts in the doc use that close *instead of*
  a link, not as well as.

---

## Two exemplars, from the published doc

Blog-linked, standard-anchored:

> A circuit breaker has one job.
>
> Stop a fault before the rest of the system pays for it.
>
> When a breaker fails to trip, the consequences move fast.
> → Equipment damage.
> → Fire risk.
> → Extended downtime.
>
> That's why breaker testing exists.
>
> Testing verifies that the breaker will actually operate under fault conditions, not just look
> functional during a visual inspection. It checks mechanical operation, insulation integrity,
> contact resistance, and trip timing.
>
> And under NFPA 70B's updated maintenance standard, breaker testing is no longer just a best
> practice. It's part of a documented electrical maintenance program.
>
> We put together a guide explaining how breaker testing works and how facilities build testing
> programs around real operational risk.
>
> Read our detailed guide on the topic here: <URL>

Hook as a challenge to look at their own site:

> Your electrical room could be a fire waiting to happen.
>
> Look inside it. Really look.
>
> Is there a box of files next to the panel? A circuit that trips every few weeks and nobody
> knows why?
>
> Here's what changes that:
> → Infrared scanning finds heat buildup inside equipment before it ignites
> → Arc flash hazard analysis to quantify the risk and show how to protect against it
> → Clean, ventilated electrical rooms remove the conditions fires need to start
>
> NFPA 70B made structured preventive maintenance mandatory in 2023. Facilities that were
> already doing this right are ahead. Those that weren't now have a safety compliance and
> insurance compliance gap.
>
> We've published an in-depth article on electrical fire prevention that you can read here:
> https://chelectric.com/electrical-fire-prevention/

---

## Output

Write `drafts/<slug>/linkedin.md`. **The post body comes first and is pasteable as-is** —
someone should be able to select from the top of the file to the separator and paste it into
LinkedIn without editing anything out. Everything else goes below a `---` separator:

```
<post body, exactly as it should appear>

---

Notes (not part of the post)
- Link is provisional until the article is live: https://chelectric.com/<url>/
- <anything a reviewer needs to know>
```

No front matter, no headings inside the post body, no markdown bold — LinkedIn renders none of
it and the asterisks show up literally in the published post.
