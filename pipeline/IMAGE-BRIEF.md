# Hero image briefs

**Current status: no image-generation connector is installed in this org** (checked
2026-09-10). See `PLAYBOOK.md` §6. Until one is added, the draft run writes a brief and a
human supplies the file.

## What the draft run produces

`drafts/<slug>/image-brief.md` containing:

1. **Generation prompt** — ready to paste into whatever image tool the human uses. Describe
   the scene concretely: subject, setting, lighting, camera framing. Name the 16:9 aspect
   ratio.
2. **Composition notes** — where the subject sits in frame, what must stay clear for any text
   overlay, what to avoid.
3. **Alt text** — written for the published post, not for the generator.
4. **Text warning** — image generators render text badly. State plainly that any lettering in
   the result will likely be garbled and that reviewers should not crop in on it. Prefer
   scenes with no signage or labels in frame.

## Subject guidance

Real electrical work in real facilities: switchgear, panelboards, thermal imaging in progress,
technicians in proper PPE. Connecticut industrial and healthcare settings.

Avoid: glowing blue circuit-board abstractions, lightning bolts, handshakes, generic
office stock, anyone in PPE worn incorrectly. Incorrect PPE in a hero image on an electrical
safety post is a credibility problem, not a style one.

## Delivery

- File: `drafts/<slug>/hero.png`, 16:9, ≥1600px wide.
- Keep the full-resolution original in the repo — it becomes the WordPress featured image.
- Embed a downscaled copy in the Word doc (see `PLAYBOOK.md` §4 on the base64 ceiling).
- If no `hero.png` is present at packaging time, proceed with a placeholder and say so. A
  missing image must not block review of the text.
