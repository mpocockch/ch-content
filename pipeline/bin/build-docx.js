// Markdown -> .docx builder for C&H blog drafts.
//
//   node pipeline/bin/build-docx.js <draft.md> <out.docx>
//
// Prints "<path> <n> bytes" on success. That byte count is what you pass as
// `expectedBytes` to sharepoint_upload_file / sharepoint_update_file — see
// PLAYBOOK.md section 4. Never estimate it.
//
// `docx` is not vendored in this repo. If the require fails, install it into a
// scratch dir and re-run with NODE_PATH pointing at it:
//
//   mkdir -p /tmp/docxbuild && cd /tmp/docxbuild && npm init -y && npm install docx
//   NODE_PATH=/tmp/docxbuild/node_modules node pipeline/bin/build-docx.js in.md out.docx
const fs = require('fs');

let docx;
try {
  docx = require('docx');
} catch (e) {
  console.error(
    'build-docx: cannot find the "docx" package.\n' +
    '  mkdir -p /tmp/docxbuild && cd /tmp/docxbuild && npm init -y && npm install docx\n' +
    '  NODE_PATH=/tmp/docxbuild/node_modules node pipeline/bin/build-docx.js <in.md> <out.docx>'
  );
  process.exit(3);
}
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType } = docx;

function inline(text) {
  // Split on **bold** and emit runs.
  const parts = text.split(/(\*\*[^*]+\*\*)/g).filter(s => s !== '');
  return parts.map(p => p.startsWith('**') && p.endsWith('**')
    ? new TextRun({ text: p.slice(2, -2), bold: true })
    : new TextRun({ text: p }));
}

function build(md) {
  const lines = md.split('\n');
  const out = [];
  let i = 0;

  // Front matter: leading lines before the first "# " heading.
  const fmEnd = lines.findIndex(l => l.startsWith('# '));
  if (fmEnd > 0) {
    for (const l of lines.slice(0, fmEnd)) {
      if (l.trim() === '') continue;
      out.push(new Paragraph({
        children: [new TextRun({ text: l.trim(), size: 18, color: '666666' })],
      }));
    }
    i = fmEnd;
  }

  let para = [];
  const flush = () => {
    if (para.length) {
      out.push(new Paragraph({ children: inline(para.join(' ')), spacing: { after: 160 } }));
      para = [];
    }
  };

  while (i < lines.length) {
    const line = lines[i];

    if (line.startsWith('|')) {              // table
      flush();
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) {
        const cells = lines[i].split('|').slice(1, -1).map(c => c.trim());
        if (!cells.every(c => /^-+$/.test(c))) rows.push(cells);
        i++;
      }
      out.push(new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: rows.map((cells, ri) => new TableRow({
          children: cells.map(c => new TableCell({
            children: [new Paragraph({ children: inline(c) })],
          })),
          tableHeader: ri === 0,
        })),
      }));
      out.push(new Paragraph({ text: '' }));
      continue;
    }

    if (line.startsWith('### ')) { flush(); out.push(new Paragraph({ children: inline(line.slice(4)), heading: HeadingLevel.HEADING_3, spacing: { before: 240, after: 120 } })); }
    else if (line.startsWith('## ')) { flush(); out.push(new Paragraph({ children: inline(line.slice(3)), heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 120 } })); }
    else if (line.startsWith('# ')) { flush(); out.push(new Paragraph({ children: inline(line.slice(2)), heading: HeadingLevel.HEADING_1, spacing: { after: 200 } })); }
    else if (/^[-*] /.test(line)) {
      flush();
      let item = line.replace(/^[-*] /, '');
      while (i + 1 < lines.length && /^\s{2,}\S/.test(lines[i + 1])) { item += ' ' + lines[++i].trim(); }
      out.push(new Paragraph({ children: inline(item), bullet: { level: 0 }, spacing: { after: 80 } }));
    }
    else if (line.trim() === '') flush();
    else para.push(line.trim());
    i++;
  }
  flush();
  return new Document({ sections: [{ children: out }] });
}

const [, , src, dest] = process.argv;
if (!src || !dest) { console.error('usage: build.js <draft.md> <out.docx>'); process.exit(2); }
Packer.toBuffer(build(fs.readFileSync(src, 'utf8'))).then(buf => {
  fs.writeFileSync(dest, buf);
  console.log(`${dest} ${buf.length} bytes`);
});
