# Gemini hero-image generation — end-to-end test

**Date:** 2026-09-10
**Script:** `pipeline/bin/generate-hero-image.py`
**Repo commit under test:** d9f14b8
**Auth mode:** key mode (`GEMINI_API_KEY` present in the environment; `GEMINI_AUTH` unset)

## Verdict

**The success path works.** The script picked a model, called the API, and wrote a real
photographic image. Exit code 0, empty stderr, no fallback triggered.

Two caveats worth knowing before this goes into the pipeline — see "Caveats" below.

## Command

```
python3 pipeline/bin/generate-hero-image.py /tmp/hero-prompt.txt /tmp/hero.png
```

Prompt used (a realistic C&H subject, not a toy prompt):

> A wide 16:9 documentary photograph of an industrial electrician in correct arc-flash
> personal protective equipment inspecting an open 480-volt switchboard inside a
> Connecticut manufacturing plant. Natural light from high windows, cool industrial
> tones, shallow depth of field, no text or signage visible in frame.

## Result

| Field | Value |
| --- | --- |
| Exit code | `0` |
| stdout | `wrote /tmp/hero.png (760159 bytes) using gemini-3-pro-image-preview` |
| stderr | *(empty)* |
| Model used | `gemini-3-pro-image-preview` — first entry in `PREFERRED`, so the key exposes it |
| Byte size | 760,159 bytes |
| Actual format | **JPEG** (JFIF 1.01, baseline, 300×300 DPI, 3 components) per `file` |
| Dimensions | 1376 × 768 px (aspect 1.792 — near 16:9, not exact) |
| SHA-256 | `06ff950f65d21fbde6a51955de4e42330ad5bc7f61584b465145d38cfd9259c8` |

`PIL` is not installed in this container, so dimensions and format come from `file(1)`.

## What the image actually depicts

Viewed directly, not inferred from metadata. It is a genuine photorealistic image, not an
error page or a placeholder: a lone electrician stands in profile at an open grey
electrical enclosure inside a large, weathered industrial hall, high clerestory windows
throwing cool blue-grey daylight behind him, machinery receding out of focus on both
sides. He holds an orange handheld multimeter and has one test lead into the panel's
interior. Composition and tonality match the brief well.

**PPE — mostly right, not textbook.** He wears a tan arc-rated coat, light leather work
gloves, and a hard hat with a gold-tinted arc-flash face shield and a head sock under it.
That reads as credible arc-flash gear at a glance. But it is not what you would specify
for an energized 480 V switchboard task: it is a coat-and-shield combination rather than a
full arc-flash suit and hood, there are no visible rubber insulating gloves under leather
protectors (the gloves look like plain leather work gloves), and the neck and lower face
are not fully enclosed by the shield. A trade audience — which is C&H's audience — could
plausibly notice. **Any hero image generated this way needs a PPE sanity check by a human
before it ships.**

**Text in frame — the instruction was not fully honored.** No large signage, but there are
small illegible label-like marks: a placard with red lettering on the open panel door, a
white label on the enclosure face, faint smudged character-like marks on the wall above
the windows, and some blurred lettering on machinery at the right edge. None of it is
readable, so none of it is embarrassingly garbled, but it is not a clean "no text" frame.

## Caveats

1. **The output is JPEG bytes written to a `.png` filename.** The script accepts PNG,
   JPEG, or WEBP magic bytes and writes the API's bytes through verbatim without
   transcoding, so `hero.png` here is really a JPEG. Anything downstream that trusts the
   extension (an upload content-type, a CMS that sniffs, a checker that requires PNG) will
   be looking at a mislabeled file. Not fixed here — flagged only, per the scope of this
   test.
2. **Aspect is 1376 × 768 (1.792), not a strict 16:9** (which would be 1365 × 768 at that
   height). Close, but crop-sensitive layouts should not assume exactness.

## Files

- `hero.png` — the generated image, byte-identical to the script's output (SHA-256 above).
