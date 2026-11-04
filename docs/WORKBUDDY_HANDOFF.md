# WorkBuddy 与 GitHub 交接说明

## 中文交接请求

以下文字可交给 WorkBuddy，并将本仓库的实际目录填入“本地目录”。

```text
请将已经准备好的 literature-sharing skill 发布到我的 GitHub。
本地目录：填写解压后含 SKILL.md 和 README.md 的目录
建议仓库名：literature-sharing
可见性：公开

请先读取 README.md 和本文件，检查整个仓库的实际文件清单，
确认只含 skill、自编脚本、说明、模板和模拟示例。
不得将目录外的论文原文、个人案例、文献分享成稿、截图、
证据台账、账号信息或本机绝对路径带入公开仓库。

上传解压后的仓库内容，让 README.md、SKILL.md、LICENSE 等位于仓库根目录。
请检查 GitHub 连接、目标账号与是否已有同名仓库；遇到同名仓库先核对，
不要覆盖其他项目，也不要强制推送。

运行 python -m unittest discover -s tests -v。
可使用本文件提供的中英文描述、Topics及发布说明。
按当前环境的实际授权完成发布，并返回仓库链接、分支及可选的发布页链接。
若缺少连接或发布权限，明确告知需要完成的操作。
```

本文件是交接说明，不会自行创建仓库或调用GitHub。上面公开发布请求仅在你主动交给 WorkBuddy 时使用；当前打包操作没有执行上传。

## English handoff request

```text
Publish the prepared literature-sharing skill to my GitHub account.
Local directory: supply the extracted folder containing SKILL.md and README.md
Suggested repository name: literature-sharing
Visibility: public

Read README.en.md and this handoff. Inspect the actual repository contents.
Include only the skill, original code/docs, templates and synthetic examples.
Do not upload papers, personal examples, generated summaries, screenshots,
private ledgers, credentials or machine-specific paths from outside this package.

Upload the extracted contents with SKILL.md, README.md and LICENSE at repository root.
Check the connected account and whether the target repository already exists.
Do not overwrite an unrelated repository or force-push.
Run python -m unittest discover -s tests -v.
Use the suggested descriptions/topics and release notes below if helpful.
Complete publishing within the environment's actual authorization and return
the repository URL, branch and optional release URL. Report any missing connection.
```

## 建议仓库资料 Suggested repository metadata

**Name:** `literature-sharing`

**中文描述：** 优先分析论文Markdown，推荐用MinerU从PDF转换；结合原PDF截图与核验，制作中文Word文献分享稿。

**English description:** Markdown-first AI skill for Chinese journal-club Word documents; use MinerU for PDF conversion and keep the original PDF for screenshots and verification.

**Topics:** `ai-skill`, `journal-club`, `literature-review`, `research-workflow`, `docx`, `pdf`, `chinese`, `academic-writing`

建议的首次提交信息 / Suggested first commit:

```text
feat: add bilingual literature-sharing skill, screenshot-only tables and push-length budget
```

## 发布说明 Suggested release notes (v0.2.0)

### 中文

- 八部分文献分享流程，默认生成中文Word。
- 三条硬性惯例：表格只截图（表体不译不重建）、结果与讨论子标题逐条忠实原文、按公众号推送密度控制篇幅。
- 配对学习原文与已有分享稿，按证据概括背景、方法、结果、讨论与政策含义。
- 全部主文图表和公式覆盖、中文题注、符号解释及正文引用要求。
- PDF渲染裁剪、来源哈希记录、Word覆盖/摘要/原生表格/篇幅检查工具。
- 中英文使用说明、安装方法、提纲和GitHub协作文件。
- 模拟测试；不包含第三方论文或个人训练材料。

### English

- Eight-part workflow for Chinese journal-club DOCX documents.
- Three hard conventions: screenshot-only tables, source-faithful Results/Discussion subheadings, and a push-length word budget.
- Paired-example editorial learning with source-grounded synthesis.
- Complete main-text figure/table/equation coverage and translated captions.
- PDF asset export with provenance and DOCX coverage/abstract utilities.
- Bilingual documentation, installation instructions, outlines and GitHub templates.
- Synthetic tests; no third-party papers or personal training materials included.

## 上传前核对 Before publishing

- 文件根目录正确，链接能在GitHub相对路径下解析。
- 不把交付ZIP本身当成全部仓库内容。
- `.gitignore` 已忽略常见论文与生成文件，但仍检查所有实际上传项。
- MIT许可仅适用于本仓库自编内容；若增加第三方材料，应另行核实其分发条件。
- 发布版本号按实际改动调整；不要把本地测试通过写成已经通过GitHub CI。
