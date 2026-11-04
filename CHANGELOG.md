# 更新记录 Changelog

## 0.2.1 — 2026-11-04

- 明确正文分析以Markdown为主，原PDF用于公式、图表截图及内容核验。 / Clarify Markdown-first analysis with PDF screenshots and verification.
- 在中英文介绍、技能输入说明及仓库描述中推荐先用MinerU将PDF转为Markdown，同时保留PDF和配套图片资源。 / Recommend MinerU PDF-to-Markdown conversion in bilingual introductions and input guidance, retaining the PDF and associated images.
- 说明仅有Markdown时的截图与版面核验边界；MinerU不内置、不自动安装。 / Document Markdown-only limitations; MinerU is not bundled or automatically installed.
- README 改为中英双语全文：GitHub 落地页同时呈现完整的英文与中文介绍，顶部提供语言跳转与 MIT/CI 徽章。 / README is now fully bilingual, so the landing page carries the complete English and Chinese introductions with language anchors and badges.
- 重写安装与调用文档：WorkBuddy 用户级目录 `%USERPROFILE%\.workbuddy\skills\`、PowerShell 复制命令、生效条件、三种调用方式、可直接粘贴的调用模板与故障排查表。 / Rewrote the installation guide with the real WorkBuddy user-level path, copy commands, activation rules, three invocation styles, a paste-ready prompt and troubleshooting.

## 0.2.0 — 2026-11-04

### 新增 Added

- 篇幅预算与压缩手法。 / Word budget and compression tactics.

### 变更 Changed

- **表格改为“只截图”**：表与图同等处理，中文表名在截图上方、中文注释在下方，表体保持原文，不再重建为 Word 原生表格、不再翻译表头与单元格。 / Tables are screenshots only; the table body stays in the original language and is never rebuilt as a native Word table.
- **结果与讨论的子标题必须忠实原文**：数量、顺序、含义逐条对应，不得增删、合并、拆分或改写；原文无子标题时也不加子标题。 / Results and Discussion subheadings now mirror the source one-to-one.
- **新增篇幅预算**：背景 300–450、方法 600–900、结果 800–1200、讨论 350–550、结论 250–400 字，正文合计 2500–3500（上限 4200），并给出五条压缩手法，面向公众号推送。 / Added a word budget and compression tactics for WeChat-push use.
- 写作细则补充“标题忠实原文”对照表、表格截图规范、常见排版缺陷（图注跨页、表格首行落页底、标题悬空）。 / Authoring guide extended with heading-fidelity rules, table screenshot rules and layout pitfalls.
- `check_share.py` 新增 `native_tables`、`body_cjk_chars` 统计与 `--max-body-chars` 参数，用于提示原生表格与超预算篇幅；新增对应单元测试（4→5 项）。 / Checker now reports native tables and approximate body length.
- 记录一次真实端到端交付暴露的三类返工原因与修正。 / Documented the three failures from a real end-to-end delivery.

## 0.1.0 — 2026-11-04

### 新增 Added

- 中文Word文献分享的八部分结构与证据核对流程。 / Eight-part Chinese DOCX journal-club workflow.
- 配对案例学习、完整图表题注、公式符号解释与逐页视觉验收规则。 / Paired-example learning, full captions, equation symbols and visual QA.
- PDF整页渲染与裁剪脚本、Word结构/证据引用/摘要检查脚本。 / PDF asset and DOCX coverage/abstract utilities.
- 中英文仓库文档、安装与WorkBuddy交接说明、模板和模拟测试。 / Bilingual docs, installation/handoff guides, templates and synthetic tests.

本版本不含真实论文或个人案例；GitHub发布由使用者后续执行。

No real papers or personal examples are included. GitHub publishing is a separate user-directed action.
