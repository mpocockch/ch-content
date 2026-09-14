import { Document, Packer, Paragraph, HeadingLevel, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType } from "docx";
import fs from "node:fs";
import crypto from "node:crypto";

const src = process.argv[2], dst = process.argv[3];
const md = fs.readFileSync(src, "utf8");
const lines = md.split("\n");

const runs = (text) => {
  const out = [];
  text.split(/\*\*(.+?)\*\*/s).forEach((part, i) => {
    if (part) out.push(new TextRun({ text: part, bold: i % 2 === 1 }));
  });
  return out.length ? out : [new TextRun("")];
};

const children = [];
let i = 0, buf = [];
const flush = () => { if (buf.length) { children.push(new Paragraph({ children: runs(buf.join(" ")) })); buf = []; } };

// leading metadata block
while (i < lines.length && !lines[i].startsWith("#")) {
  if (lines[i].trim())
    children.push(new Paragraph({ children: [new TextRun({ text: lines[i].trim(), italics: true, size: 18, color: "595959" })] }));
  i++;
}

for (; i < lines.length; i++) {
  const s = lines[i].trim();
  if (s.startsWith("|")) {
    flush();
    const rows = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) {
      const cells = lines[i].trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim());
      if (!cells.every(c => /^:?-{2,}:?$/.test(c))) rows.push(cells);
      i++;
    }
    i--;
    children.push(new Table({
      width: { size: 100, type: WidthType.PERCENTAGE },
      rows: rows.map((r, ri) => new TableRow({
        children: r.map(c => new TableCell({
          children: [new Paragraph({ children: ri === 0 ? [new TextRun({ text: c, bold: true })] : runs(c) })],
        })),
      })),
    }));
    children.push(new Paragraph({ text: "" }));
  }
  else if (s.startsWith("### ")) { flush(); children.push(new Paragraph({ children: runs(s.slice(4)), heading: HeadingLevel.HEADING_3 })); }
  else if (s.startsWith("## "))  { flush(); children.push(new Paragraph({ children: runs(s.slice(3)), heading: HeadingLevel.HEADING_2 })); }
  else if (s.startsWith("# "))   { flush(); children.push(new Paragraph({ children: runs(s.slice(2)), heading: HeadingLevel.HEADING_1 })); }
  else if (s.startsWith("- "))   { flush(); children.push(new Paragraph({ children: runs(s.slice(2)), bullet: { level: 0 } })); }
  else if (!s) flush();
  else buf.push(s);
}
flush();

const doc = new Document({ creator: "C&H Electric Blog Pipeline", sections: [{ children }] });
const bufOut = await Packer.toBuffer(doc);
fs.writeFileSync(dst, bufOut);
console.log("bytes:", bufOut.length);
console.log("sha256:", crypto.createHash("sha256").update(bufOut).digest("hex"));
console.log("b64len:", bufOut.toString("base64").length);
console.log("paragraphs:", children.length);
