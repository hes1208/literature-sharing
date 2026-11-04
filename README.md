# Literature Sharing 文献分享 Skill

[English](#english) · [简体中文](#中文)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Validate utilities](https://github.com/hes1208/literature-sharing/actions/workflows/validate.yml/badge.svg)](https://github.com/hes1208/literature-sharing/actions/workflows/validate.yml)

---

# English

Turn a research paper into a **Chinese Word journal-club / WeChat-push document** with verifiable evidence and complete figures. Optionally learn the user's editorial style from paired source papers and previous DOCX summaries.

It is an instruction package for AI assistants, shipped with two utility scripts. It is **not** a standalone automated scientific summarizer.

## What it produces

A fixed eight-part Chinese document:

1. **Paper information** — original title, authors, affiliations, journal, publication date, DOI link.
2. **Abstract** — complete Chinese translation, never compressed into a summary.
3. **Background and objectives** — the introduction's core logic, 300–450 characters.
4. **Methods** — data, sample construction, measurement logic, original equation screenshots with every symbol defined.
5. **Results** — main findings only, citing **every** figure and table with key numbers, 800–1200 characters.
6. **Discussion** — each theme's conclusion and reasoning chain.
7. **Conclusions or policy implications** — only when the paper supports them.
8. **Original English abstract** — copied verbatim.

## Three non-negotiable conventions

1. **Tables are screenshots only.** A Chinese table title sits above the screenshot and Chinese notes below; the table body stays in the original language. Never rebuild a table as a native Word table and never translate its header or cells — rebuilding invites transcription errors, distorts merged cells, and breaks the reader's ability to check the paper cell by cell.
2. **Headings follow the source.** Results and Discussion subheadings mirror the original one-to-one — same count, same order, same meaning, translated only. Never invent, merge, split or re-theme them. If the source has no subheadings, add none.
3. **Write at push density.** Background 300–450, methods 600–900, results 800–1200, discussion 350–550, conclusions 250–400 characters; total body 2500–3500 (hard cap 4200). Abstract translation and caption notes are never compressed.

Complete figure/table coverage, checkable numbers and per-symbol equation explanations remain mandatory.

## Recommended input: Markdown analysis + PDF verification

**Read the paper from Markdown and keep the original PDF alongside it.** The division of labour is fixed:

- **Markdown** — full-text reading, background logic, methods, results, discussion, abstract translation, and transcription of the original subsection headings. Tables arrive as HTML and equations as LaTeX, which makes value checking straightforward.
- **PDF** — screenshots of equations, figures and tables, plus verification of layout, legends, caption boundaries, quantities and suspected OCR errors. **It is the only trusted source for screenshots.**

Workflow: `PDF → MinerU → Markdown analysis + PDF screenshots → Word`.

If you only have a PDF, convert it first with [MinerU](https://github.com/opendatalab/MinerU) (CLI `magic-pdf` or the official web version), keeping the PDF and its image assets:

```bash
magic-pdf -p paper.pdf -o ./work
```

Four caveats with MinerU output: images are **remote links** (`cdn-mineru…`), not local files, so artwork must still be captured from the PDF; multi-column text may be merged into one line with broken words; long captions may be split into interleaved fragments; some tables arrive as several `<table>` blocks.

Markdown alone supports textual analysis, but without the original PDF the screenshots and layout cannot be claimed as verified. MinerU is not bundled, not installed automatically, and this recommendation never uploads a paper to an external service on its own.

## Quick start

```text
Use $literature-sharing to produce a Chinese share document.

Paper Markdown: /path/to/paper.md   (recommended: converted from the PDF with MinerU)
Paper PDF:      /path/to/paper.pdf  (required for screenshots)
Paired examples (optional): /path/to/examples
Output directory: /path/to/output

Requirements:
1. Tables as screenshots only — do not translate the table body, do not rebuild tables in Word.
2. Translate the original Results/Discussion subheadings one-to-one; add or drop none.
3. Keep the prose inside the push-length budget.
4. Include every figure and table and cite each one with its key numbers.
5. Render and inspect every final page before delivery.
```

## Install and invoke

- **Portable** — put the folder anywhere and ask the assistant to read `SKILL.md` by absolute path.
- **WorkBuddy** — copy the runtime files into `%USERPROFILE%\.workbuddy\skills\literature-sharing`, start a **new session**, then invoke `$literature-sharing`, or simply say “turn this paper into a Chinese journal-club Word document”.
- **Codex and similar hosts** — copy into the configured skills directory (usually `~/.codex/skills`).

Step-by-step commands, activation rules and troubleshooting: [docs/INSTALLATION.en.md](docs/INSTALLATION.en.md).

## Repository layout

```text
literature-sharing/
├── SKILL.md                     Core rules (bilingual)
├── agents/openai.yaml           UI metadata for hosts supporting the format
├── references/                  Writing guide, terminology, delivery checklist
├── templates/                   Chinese and English outlines
├── scripts/pdf_assets.py        Whole-page rendering and precise cropping
├── scripts/check_share.py       DOCX coverage, abstract, table and length checks
├── examples/                    Synthetic crop plan and evidence ledger
├── tests/                       Synthetic PDF/DOCX tests, no real papers
├── docs/                        Installation, utilities, validation, handoff
├── .github/                     CI workflow, issue and PR templates
├── requirements.txt · CONTRIBUTING.md · CHANGELOG.md · LICENSE
```

## Utilities

Python 3.10+. Dependencies: `Pillow`, `pypdfium2`, `python-docx`.

```bash
python -m pip install -r requirements.txt
python scripts/pdf_assets.py --pdf work/paper.pdf --out-dir work/pages --render-pages 1 2
python scripts/pdf_assets.py --pdf work/paper.pdf --plan work/crop-plan.json --out-dir work/assets
python scripts/check_share.py --docx outputs/share.docx --ledger work/evidence-ledger.json --abstract-file work/abstract.txt --max-body-chars 4200
python -m unittest discover -s tests -v
```

Crop coordinates and ledger entries must be built for the actual paper. The checker never judges scientific interpretation, translation accuracy, screenshot content or visual layout — those remain the assistant's job. See [docs/TOOLS.md](docs/TOOLS.md) and [docs/VALIDATION.md](docs/VALIDATION.md).

## Host compatibility and scope

- Rules are plain Markdown; no cloud service, account, API key or paid plugin is required.
- DOCX generation and rendering rely on the host's existing tools; no Word, LibreOffice or standalone renderer is bundled.
- Default output is Chinese Word. English documents explain the same structure for collaboration; they do not switch the deliverable to a bilingual full text.
- Faithful abstract translation, evidence preservation, correlation-versus-causation discipline, documented source inconsistencies and page-by-page visual inspection are delivery requirements, not optional polish.

## License

Original instructions, documentation and scripts are MIT licensed. The licence grants no right to redistribute third-party papers, figures or case materials. See [CONTRIBUTING.md](CONTRIBUTING.md) for feedback and changes.

---

# 中文

将研究论文制作成有证据、有图表、可直接使用的**中文 Word 文献分享稿**。可结合“原文 + 以往分享稿”学习个人写法，同时保留公式、全部主文图表、完整中文题注和正文引用。

它是 AI 助手的任务指令包，附带两个辅助脚本；**不是独立运行的论文自动总结软件**。适用于组会、文献汇报、论文精读和中文科研分享。

## 输出什么

固定的八部分结构：

1. **文章信息** —— 原文标题、原文作者、作者机构、原文期刊、发表日期、原文链接。
2. **摘要** —— 完整中文翻译，不压缩成摘要总结。
3. **研究背景与研究目的** —— 引言的核心逻辑，300–450 字。
4. **研究方法** —— 数据、样本构建、测度逻辑，原文公式截图并逐符号解释。
5. **研究结果** —— 只写主要发现，**每张**图与表都在正文中被引用并给出关键数值，800–1200 字。
6. **讨论** —— 各部分的结论与推理链。
7. **结论或政策建议** —— 仅在原文支持时保留。
8. **原文英文摘要** —— 直接复制核对。

## 三条硬性惯例

1. **表格只截图。** 中文表名在截图上方、中文注释在下方，表体保持原文语言。不重建为 Word 原生表格、不翻译表头与单元格——重建会引入抄录错误、扭曲合并单元格，并破坏读者逐格对照原文的能力。
2. **标题忠实原文。** 结果与讨论的子标题与原文逐条对应（数量、顺序、含义一致），只译不改，不新增、不合并、不拆分、不改写主题；原文没有子标题，分享稿也不加。
3. **按推送密度写作。** 背景 300–450 字、方法 600–900、结果 800–1200、讨论 350–550、结论 250–400，正文合计 2500–3500（上限 4200）；摘要译文与图表题注不参与压缩。

图表一张不漏、数值可核对、公式符号逐个解释，是三条惯例之外不变的前提。

## 推荐输入：Markdown 分析 + PDF 核验

**推荐基于 Markdown 分析正文，并同时提供原始 PDF。** 分工固定：

- **Markdown** —— 阅读全文、梳理引言逻辑、方法、结果、讨论，翻译摘要，抄录原文小节标题。表格已转为 HTML、公式已转为 LaTeX，便于逐格核对数值。
- **PDF** —— 截取公式、图和表，核对版面、图例、题注边界、数值与 OCR 可疑项。**这是截图与核验的唯一可信来源。**

流程：`论文 PDF → MinerU 转换 → Markdown 正文分析 + PDF 截图核验 → Word 分享稿`。

若只有 PDF，建议先用 [MinerU（官方项目）](https://github.com/opendatalab/MinerU) 转换（命令行 `magic-pdf` 或官方在线版），并保留原始 PDF 及其图片资源：

```bash
magic-pdf -p paper.pdf -o ./work
```

使用 MinerU 输出须注意四点：**图片是远程链接**（`cdn-mineru…`），不是本地文件，成稿插图仍须回 PDF 截图；跨栏文字可能被拼成一行并断词；长图注可能被拆成多段并与正文交错；少数表格会被拆成多个 `<table>` 片段。

仅有 Markdown 时可推进文字分析，但缺少原始 PDF 就不能声称已完成截图与版面核验。MinerU 不内置、不自动安装，也不会因该建议自动上传论文到外部服务。

## 快速开始

```text
用 $literature-sharing 做这篇论文的中文分享稿。

论文 Markdown：/path/to/paper.md（推荐先用 MinerU 从 PDF 转换）
论文 PDF：     /path/to/paper.pdf（截图必需）
案例目录（可选）：/path/to/examples
输出目录：/path/to/output

要求：
1. 表只截图，不要翻译表体，也不要重建为 Word 表格；
2. 结果和讨论的小标题照原文逐条翻译，不增不减；
3. 正文按公众号推送长度控制；
4. 图和表全部收录，并在正文中逐张引用、给出关键数值；
5. 交付前逐页渲染检查排版。
```

## 安装与调用

- **直接读取** —— 把目录放在助手可访问的位置，提供 `SKILL.md` 绝对路径即可，无需安装。
- **WorkBuddy** —— 将运行时文件复制到 `%USERPROFILE%\.workbuddy\skills\literature-sharing`，**新开会话**，然后 `$literature-sharing`，或直接说“把这篇文章做成中文文献分享 Word”。
- **Codex 等宿主** —— 放入配置的技能目录（通常为 `~/.codex/skills`）。

逐步命令、生效条件与故障排查：[docs/INSTALLATION.zh-CN.md](docs/INSTALLATION.zh-CN.md)。

## 仓库结构

```text
literature-sharing/
├── SKILL.md                     核心规则（中英对照说明）
├── agents/openai.yaml            支持该格式宿主的界面元数据
├── references/                   写作细则、术语、交付检查
├── templates/                    中文与英文结构提纲
├── scripts/pdf_assets.py         PDF 整页渲染与精确裁剪
├── scripts/check_share.py        Word 覆盖、摘要、原生表格与篇幅检查
├── examples/                     纯模拟的裁剪方案与证据台账
├── tests/                        模拟 PDF/DOCX 测试，不含真实论文
├── docs/                         安装、脚本、验证与交接说明
├── .github/                      CI 工作流、Issue 与 PR 模板
├── requirements.txt · CONTRIBUTING.md · CHANGELOG.md · LICENSE
```

## 辅助脚本

Python 3.10 及以上，依赖 `Pillow`、`pypdfium2`、`python-docx`。

```bash
python -m pip install -r requirements.txt
python scripts/pdf_assets.py --pdf work/paper.pdf --out-dir work/pages --render-pages 1 2
python scripts/pdf_assets.py --pdf work/paper.pdf --plan work/crop-plan.json --out-dir work/assets
python scripts/check_share.py --docx outputs/share.docx --ledger work/evidence-ledger.json --abstract-file work/abstract.txt --max-body-chars 4200
python -m unittest discover -s tests -v
```

裁剪坐标与台账必须按当前论文制定。检查脚本不判定科学解释、翻译正确性、截图内容与视觉排版，这些仍由助手逐项核对。详见 [docs/TOOLS.md](docs/TOOLS.md) 与 [docs/VALIDATION.md](docs/VALIDATION.md)。

## 宿主兼容性与边界

- 规则为普通 Markdown，不要求云服务、账号、API 或付费插件。
- Word 生成与渲染使用宿主已有工具；本仓库不捆绑 Word、LibreOffice 或独立渲染器。
- 默认输出中文 Word；英文文档用于协作与理解，不把交付物改成双语全文。
- 忠实翻译摘要、保留证据、区分相关与因果、标注原文矛盾、逐页视觉检查，是交付要求而非可选润色。

## 许可

自编指令、文档与脚本采用 MIT 许可；该许可不授予第三方论文、图片或案例的再分发权。反馈与改进见 [CONTRIBUTING.md](CONTRIBUTING.md)。
