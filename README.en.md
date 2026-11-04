# Literature Sharing Skill

English · [简体中文](README.md)

> This file mirrors the English half of the bilingual [README.md](README.md#english). When the two differ, the bilingual README is authoritative.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Validate utilities](https://github.com/hes1208/literature-sharing/actions/workflows/validate.yml/badge.svg)](https://github.com/hes1208/literature-sharing/actions/workflows/validate.yml)

> **中文摘要** —— 一个 AI 助手指令包，把论文转成中文组会／公众号 Word 分享稿。以 Markdown 为阅读载体（只有 PDF 时先用 MinerU 转换），原始 PDF 始终是截图与核验的依据。固定八部分结构：文献信息、摘要完整翻译、精简背景、含公式截图与逐符号释义的方法、逐图逐表引用的结果、讨论、结论、原文英文摘要。三条硬性惯例：**表格只截图**（不重建、不译表体）、**结果与讨论子标题逐条对应原文**、**正文控制在推送可读字数内**。中文完整说明见 [README.md](README.md)。

Create a **Chinese journal-club Word document** from a research paper. Optionally learn the user's editorial style from paired source papers and previous DOCX summaries. Preserve original equation screenshots, every main-text figure/table, complete Chinese captions and notes, and narrative references to each object.

This is an instruction package for an AI assistant with two utility scripts. It is not a standalone automated scientific summarizer.

## Recommended input: Markdown analysis + MinerU conversion

**Analyze the paper primarily from Markdown and provide the original PDF alongside it.** The division of labour is fixed:

- **Markdown:** full-text reading, background logic, methods, results, discussion, abstract translation, and transcription of the original subsection headings. Tables arrive as HTML and equations as LaTeX, which makes value checking straightforward.
- **PDF:** screenshots of equations, figures and tables, plus verification of layout, legends, caption boundaries, quantities and suspected OCR errors. **It is the only trusted source for screenshots.**

Recommended workflow: `PDF → MinerU → Markdown analysis + PDF screenshots/verification → Word summary`.

If you only have a PDF, convert it with [MinerU (official project)](https://github.com/opendatalab/MinerU) first — either the `magic-pdf` CLI or the official web version — and keep the original PDF and its image assets:

```bash
magic-pdf -p paper.pdf -o ./work
```

Four caveats when using MinerU output: images are **remote links** (`cdn-mineru…`), not local files, so deliverable artwork must still be captured from the PDF; multi-column text may be merged into one line with broken words; long captions may be split into interleaved fragments; and some tables are split into several `<table>` blocks.

Markdown alone supports textual analysis, but without the original PDF you cannot claim the screenshots and layout have been verified. PDF-only text extraction is a fallback. MinerU is not bundled, not installed automatically, and this recommendation never uploads a paper to an external service on its own.

## Deliverable

1. Paper information: original title, authors, affiliations, journal, publication date, original link.
2. Complete Chinese translation of the abstract.
3. Concise background and objectives, combined or separate as appropriate.
4. Major methods, their logic, original equation screenshots and all symbol definitions.
5. Main findings, all main-text figure/table screenshots, translated captions/notes and explicit narrative citations.
6. Discussion conclusions and reasoning, when present.
7. Author-supported conclusions or policy implications, following the actual paper.
8. Original English abstract, copied and verified without paraphrasing.

Figure titles and notes go below figures; table titles go above tables and notes below.

## Three non-negotiable conventions

1. **Tables are screenshots only.** A Chinese table title sits above the screenshot and Chinese notes below it; the table body stays in the original language. Never rebuild a table as a native Word table and never translate its header or cells.
2. **Headings follow the source.** Results and Discussion subheadings mirror the original one-to-one — same count, same order, same meaning, translated only. If the source has no subheadings, add none.
3. **Write at WeChat-push density.** Background 300–450, methods 600–900, results 800–1200, discussion 350–550, conclusions 250–400 Chinese characters; total body 2500–3500 (hard cap 4200). The abstract translation and caption notes are never compressed.

Full figure/table coverage, verifiable numbers and per-symbol equation explanations remain mandatory.

## Usage

Load [SKILL.md](SKILL.md) in an assistant supporting local skills, or ask an assistant to read that file directly.

```text
Use $literature-sharing.
Main text: /path/to/paper.md (preferably converted from PDF with MinerU)
Screenshots and verification: /path/to/paper.pdf; keep associated Markdown images
Optional paired examples: /path/to/examples
Output directory: /path/to/output
Create a Chinese Word journal-club document using the eight-part structure.
Screenshot both figures and tables (leave table bodies untranslated),
translate the original Results/Discussion subheadings verbatim,
keep the prose inside the push-length budget, and inspect every final rendered page.
```

Examples are optional. PDF text extraction can replace Markdown when necessary. Skill discovery and installation are host-specific; `$literature-sharing` is not a universal command.

Installation: [English](docs/INSTALLATION.en.md) · [中文](docs/INSTALLATION.zh-CN.md)

## Files

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Main operational instructions with an English summary |
| [agents/openai.yaml](agents/openai.yaml) | Optional metadata for compatible hosts |
| [references/authoring-guide.md](references/authoring-guide.md) | Detailed editorial and evidence rules |
| [references/quality-checklist.md](references/quality-checklist.md) | Scientific, screenshot, layout and delivery checks |
| [references/terminology.md](references/terminology.md) | Contextual terminology checks |
| [templates/share-outline.en.md](templates/share-outline.en.md) | English explanation of the default Chinese structure |
| [templates/share-outline.zh-CN.md](templates/share-outline.zh-CN.md) | Chinese writing outline |
| [docs/TOOLS.md](docs/TOOLS.md) | Script usage and limitations |
| [docs/WORKBUDDY_HANDOFF.md](docs/WORKBUDDY_HANDOFF.md) | Bilingual GitHub upload handoff |
| scripts/ | PDF cropping and DOCX coverage checks |
| examples/ | Synthetic crop plan and evidence ledger |
| tests/ | Synthetic PDF/DOCX tests; no real papers |

## Utilities

Python 3.10+ with `Pillow`, `pypdfium2` and `python-docx`. Use a host-provided runtime or your own virtual environment.

```bash
python -m pip install -r requirements.txt
python scripts/pdf_assets.py --pdf work/paper.pdf --out-dir work/pages --render-pages 1 2
python scripts/pdf_assets.py --pdf work/paper.pdf --plan work/crop-plan.json --out-dir work/assets
python scripts/check_share.py --docx outputs/share.docx --ledger work/evidence-ledger.json --abstract-file work/abstract.txt --max-body-chars 4200 --report work/check.json
python -m unittest discover -s tests -v
```

Replace synthetic example coordinates and ledger entries with verified paper evidence. Passing a mechanical check does not verify scientific interpretation, translation, screenshot completeness or page layout.

See [local validation](docs/VALIDATION.md) for completed checks and their limits.

## Compatibility and limits

The main skill is ordinary Markdown, with no mandatory cloud account or proprietary connector. DOCX authoring and rendering require tools supplied by the host; no renderer is bundled. Other assistants can read `SKILL.md` even if they do not support the optional metadata.

WorkBuddy import paths, GitHub integrations and publication capabilities must be checked in the actual environment. This repository does not claim a verified WorkBuddy installation API. The default output remains Chinese; bilingual documentation supports distribution and collaboration.

All main-text figures and tables are in scope by default. Supplementary material follows the user's request and the files actually provided. Never claim to have read unavailable material. Render and inspect all pages before claiming layout approval.

## Publishing

Upload the repository contents, not just its ZIP archive. Suggested repository name: `literature-sharing`. See the [bilingual handoff](docs/WORKBUDDY_HANDOFF.md) for descriptions, topics and a ready-to-use WorkBuddy request.

No original papers, personal training cases, finished summaries, machine-specific paths or private ledgers are included. Review the actual upload list as well as `.gitignore`.

## License and contributions

Original instructions, documentation and code are available under the [MIT License](LICENSE). This license does not grant rights to third-party papers, figures or examples. See [CONTRIBUTING.md](CONTRIBUTING.md).
