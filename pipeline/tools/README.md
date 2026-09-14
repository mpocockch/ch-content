# pipeline/tools

## `md2docx.mjs`

Turns a `drafts/<slug>/draft.md` into a `.docx` for the SharePoint Blog folder.

```
npm install docx          # into a scratch dir, not this repo
node md2docx.mjs <draft.md> <out.docx>
```

It prints `bytes`, `sha256` and `b64len`. **Pass the `bytes` value as `expectedBytes` on the
upload call** — see `PLAYBOOK.md` §4.

Why this and not hand-assembled XML: a `.docx` that unzips cleanly and whose parts parse as
well-formed XML can still be invalid OOXML, and Word and Graph will both refuse it. On
2026-09-14 a hand-rolled builder that omitted the required `<w:tblGrid>` element produced an
8,475-byte file that passed both of those checks and would not open, while a 15,407-byte file
from this script opened fine. Use the `docx` library.

Handles: the leading metadata block, `#`/`##`/`###` headings, `**bold**`, `- ` bullets, and
pipe tables. Anything else passes through as body text.

### Upload checklist

1. Build, note the byte count.
2. `sharepoint_upload_file` with `expectedBytes` set to that count.
3. `read_resource` on the returned `resourceUri`. Text back = it opens. `notSupported` = it
   does not; do not announce it as ready.
