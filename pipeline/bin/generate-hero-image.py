#!/usr/bin/env python3
"""Generate a hero image via the Gemini API.

Usage:  generate-hero-image.py <prompt-file> <output.png> [--model NAME]

Reads the API key from GEMINI_API_KEY. Exits 3 if the key is absent, which the
caller must treat as "fall back to the manual AI Studio brief" — not as an error.

Deliberately dependency-free (stdlib only): these run in fresh containers with no
install step. The key is never printed, logged, or written to disk.

Exit codes
  0  image written and validated
  2  usage error
  3  no API key -> fall back to the manual brief (NOT a failure)
  4  no image-capable model available to this key
  5  API call failed
  6  response contained no usable image data
"""

import json
import os
import sys
import urllib.error
import urllib.request

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"

# Preference order. The list is advisory: whatever this key actually exposes wins,
# so a model being renamed or retired degrades to the next choice instead of
# breaking the run. Record the model that worked in PLAYBOOK.md section 6.
PREFERRED = [
    "gemini-3-pro-image-preview",
    "gemini-2.5-flash-image-preview",
    "gemini-2.0-flash-preview-image-generation",
]

# PNG, JPEG, WEBP(RIFF) magic bytes.
MAGIC = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"RIFF")


def call(url, payload=None, timeout=180):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if data else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def redact(text, key):
    """Never let the key reach stderr via an echoed URL."""
    return text.replace(key, "***") if key else text


def pick_model(key):
    """Ask the key what it can actually use, rather than trusting a hard-coded id."""
    try:
        listing = call(f"{API_ROOT}/models?key={key}&pageSize=200")
    except urllib.error.HTTPError as e:
        print(f"could not list models: HTTP {e.code} {redact(e.read().decode()[:300], key)}",
              file=sys.stderr)
        return None

    available = {}
    for m in listing.get("models", []):
        name = m.get("name", "").removeprefix("models/")
        methods = m.get("supportedGenerationMethods", []) or []
        if "generateContent" in methods:
            available[name] = m

    for want in PREFERRED:
        if want in available:
            return want
    # Any other model advertising image output.
    for name, m in available.items():
        if "image" in name.lower() and "embedding" not in name.lower():
            return name
    print(f"no image-capable model found; key exposes: {sorted(available)[:20]}",
          file=sys.stderr)
    return None


def extract_image(resp):
    """Walk the response for the first inline base64 blob that decodes to an image."""
    import base64

    stack = [resp]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            blob = node.get("inlineData") or node.get("inline_data")
            if isinstance(blob, dict) and blob.get("data"):
                try:
                    raw = base64.b64decode(blob["data"], validate=True)
                except Exception:
                    raw = None
                if raw and raw.startswith(MAGIC):
                    return raw
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    model_override = next(
        (a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--model=")), None
    )
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    prompt_file, out_path = args

    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print("GEMINI_API_KEY not set - fall back to the manual AI Studio brief "
              "(see pipeline/IMAGE-BRIEF.md). This is not a failure.", file=sys.stderr)
        return 3

    with open(prompt_file) as f:
        prompt = f.read().strip()
    if not prompt:
        print(f"{prompt_file} is empty", file=sys.stderr)
        return 2

    model = model_override or pick_model(key)
    if not model:
        return 4

    try:
        resp = call(
            f"{API_ROOT}/models/{model}:generateContent?key={key}",
            {"contents": [{"parts": [{"text": prompt}]}]},
        )
    except urllib.error.HTTPError as e:
        body = redact(e.read().decode()[:500], key)
        print(f"generateContent failed: HTTP {e.code} {body}", file=sys.stderr)
        return 5
    except Exception as e:
        print(f"generateContent failed: {redact(str(e), key)}", file=sys.stderr)
        return 5

    raw = extract_image(resp)
    if not raw:
        # Surface any text the model returned instead - usually a refusal or a
        # safety block, which is the actionable information here.
        texts = []
        stack = [resp]
        while stack:
            n = stack.pop()
            if isinstance(n, dict):
                if isinstance(n.get("text"), str):
                    texts.append(n["text"])
                stack.extend(n.values())
            elif isinstance(n, list):
                stack.extend(n)
        print(f"no image in response from {model}. Model said: "
              f"{' | '.join(texts)[:400] or '(nothing)'}", file=sys.stderr)
        return 6

    with open(out_path, "wb") as f:
        f.write(raw)
    print(f"wrote {out_path} ({len(raw)} bytes) using {model}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
