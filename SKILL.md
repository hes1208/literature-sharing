---
name: literature-sharing
description: Create a Chinese journal-club / WeChat-push Word document using Markdown-first paper analysis, preferably converted with MinerU, and the original PDF for screenshots and verification. Optionally learn the user's style from paired papers and past Word summaries. Includes faithful abstract translation, concise synthesis, screenshot-only figures and tables, equation explanations, Chinese captions and original section headings. Use for structured 文献分享 or 论文分享稿 requests.
---

# 文献分享 Literature Sharing

将论文制作成可直接分享（组会、公众号推送）的中文 Word 稿。正文要短，但方法、图表覆盖及证据不能省略。输出语言、格式和范围以用户的当前要求为准。

Create a concise Chinese journal-club / WeChat DOCX grounded in the paper. Preserve the author's evidence and uncertainty. Follow the user's requested language, scope, and format.

## 三条硬性惯例 Three non-negotiable conventions

这三条来自实际交付后的返工意见，优先级高于任何个人偏好。

1. **表格只截图，不重制、不翻译表体。** 表与图同等对待：从 PDF 截取原表，中文表名放在截图上方，中文注释放在截图下方，编号沿用原文。禁止把表格重建为 Word 原生表格，也禁止把表头或单元格内容译成中文。重建会引入抄录错误与排版失真，并破坏"读者可逐格对照原文"这一分享前提。
2. **结果与讨论的（子）标题必须忠实原文。** 按原文章节层级与措辞逐条对应翻译，不得增删、合并、拆分，也不得按自己的主题重新归并。原文结果部分只有"Results"而无子标题时，分享稿同样不加子标题。仅"研究方法"允许做功能性切分（数据来源 / 测度 / 计量策略），但优先沿用原文小节名。
3. **按公众号推送的密度写作。** 背景与结果必须压缩到"能读、能听、能推送"的长度；摘要译文、图表题注、公式符号解释不参与压缩。

### 篇幅预算 Word budget（正文字符数，不含摘要译文与图表题注）

| 部分 | 目标 | 上限 |
| --- | --- | --- |
| 03 研究背景与目的 | 300–450 | 600 |
| 04 研究方法 | 600–900 | 1200 |
| 05 研究结果 | 800–1200 | 1500 |
| 06 讨论 | 350–550 | 700 |
| 07 结论或政策建议 | 250–400 | 500 |
| 全文正文合计 | 2500–3500 | 4200 |

超预算时按下列顺序压缩，不得靠删图表或删数值达标：

- 删除铺垫词与套话（"值得注意""大量研究表明""已有丰富文献"）。
- 同向证据合并，只报"方向 + 量级 + 比较基准"，例如"晚 10 年商业化，扩散速度高 0.02"。
- 机制细节、口径说明、稳健性检验移入图注或括号，不进正文。
- 背景严格限定四步：为何重要 → 已知什么 → 缺什么 → 本文做什么；每步 1–2 句。

## 输入与路径 Inputs

- 接受 Markdown 与 PDF 两种输入，但两者分工不同：**Markdown 是主要阅读载体**，PDF 是版面容器的唯一可信来源。
- 优先通过 Markdown 理解全文，通过 PDF 核对版面、图表、公式、作者机构、摘要及 OCR 可疑项。没有 Markdown 时可提取 PDF 文本。
- 只有 PDF 时，推荐先用 MinerU 转为 Markdown 再分析（做法与注意事项见下节）。仅有 Markdown 而无原始 PDF 时，可推进文字分析，但不得声称已完成原文截图与版面核验。
- 案例为“论文原文 + 对应分享 Word”配对。结合原文学习案例如何删减、组织结果、解释符号与使用图表，不把案例的研究事实迁移到新论文。
- 先检查实际文件清单。若明确只有一篇待分析论文，直接推进；只有影响目标论文识别或核心内容的缺失信息才需要询问。
- 不覆盖原稿；按用户输出目录另存有辨识度的 `.docx`。内部截图和核对记录放入任务临时目录。

### 推荐的 PDF→Markdown 预处理 Preprocessing with MinerU

只有 PDF 时，建议先用 [MinerU](https://github.com/opendatalab/MinerU) 转换为 Markdown（`magic-pdf` 命令行或官方在线版均可），再开始工作。理由有三：

- 表格转成 HTML `<table>`，可逐格读出数值，便于核对结果与原文是否一致（成稿仍用原文表格截图）。
- 公式转成 LaTeX，便于判断哪些是需要在成稿中截图的展示公式、哪些只是行内符号。
- 章节标题、图注保留原有顺序，便于逐条抄录 `Results` / `Discussion` 子标题作为分享稿标题。

MinerU 输出的已知偏差，使用时必须回 PDF 核对：

- **图片是远程链接（`cdn-mineru…`），不是本地文件。** 成稿插图必须回 PDF 截图，不要直接下载这些链接当图版：分辨率、裁切边界不可控，且可能包含跨栏碎片或缺失子图。
- 跨栏文字可能被拼成一行并出现断词（如 `te chnologies`），引用原句时以 PDF 为准。
- 长图注可能被拆成多段并与正文交错，拼接后需回 PDF 校对顺序与所属图号。
- 少数论文的表格会被拆成多个 `<table>` 片段，或多栏表格的单元格错位。
- 页码、行号等版面信息不保留，定位原文位置时以 PDF 页码为准。

When only a PDF is available, convert it to Markdown with MinerU first (CLI or the official web version). Markdown serves reading, table-value checking and heading extraction; the PDF remains the only trusted source for figures, tables and equations, because MinerU emits remote image links that must not be used as deliverable artwork.

## 工作流程 Workflow

1. **学习案例**：阅读可用的配对原文和 Word，归纳文章信息字段、背景篇幅、方法解释、结果粒度、讨论写法及版式。案例较多时先扫描全部，再细读方法和图表类型接近的案例；没有案例也可使用本 skill 的默认结构。
2. **核对全文**：梳理引言逻辑、方法、结果、讨论及结论。建立图、表、公式清单，记下来源页、子图、题名、注释、关键结果、正文引用和符号解释。同时抄录**原文的结果与讨论子标题原句**，作为分享稿标题的唯一依据。详细写作规则见 [authoring-guide.md](references/authoring-guide.md)。
3. **撰写与截图**：以主线组织简洁中文正文，从 PDF 截取完整公式、全部目标范围的图和**全部目标范围的表**。不要依据 Markdown 的远程图片地址猜测完整性。可使用 [pdf_assets.py](scripts/pdf_assets.py) 按裁剪清单生成截图。
4. **制作 Word**：保持可编辑的正文，插入原文截图，执行下列结构及题注位置要求。表只放截图，不进入 Word 表格对象。优先使用当前环境可用的文档生成/渲染工具；辅助脚本不负责科学总结或自动生成成稿。
5. **内容与版式验收**：逐项核对 [quality-checklist.md](references/quality-checklist.md)；核对字数是否在预算内、标题是否与原文逐条对应、表体是否保持原文。若使用清单 JSON，可运行 [check_share.py](scripts/check_share.py) 查漏；脚本通过不等于学术内容或排版已通过。
6. **交付**：返回最终 Word 的可点击绝对路径及极简说明。明确仍未解决的实质问题，不把临时截图、PDF 或核对台账当成最终交付。用户要求附加格式时再一并提供。

## 默认八部分结构 Default eight-part structure

### 1 文章信息 Paper information

严格保留六个字段：原文标题、原文作者、作者机构、原文期刊、发表日期、原文链接。作者及机构上标对应准确；优先 DOI；发表时间不得与投稿或接收日期混淆。中文分享题目可单列，原文标题保留原文。

### 2 原文摘要的中文翻译 Chinese abstract translation

完整翻译摘要，不压缩成摘要总结。专业术语、缩写、数值、单位、条件和不确定性必须准确。按本文语境决定译法，见 [terminology.md](references/terminology.md)。

### 3 研究背景与研究目的 Background and objectives

突出引言最重要的逻辑：重要性 → 已有认识 → 缺口/转折 → 本文目的。重点检查引言首句、转折句、末句，不机械摘抄。默认合并为一节 300–450 字；内容确实庞杂时可拆为“3.1 研究背景 / 3.2 研究目的与研究问题”，但两节合计仍受预算约束。

### 4 研究方法 Methods

说明每个主要方法“解决什么问题、用什么信息、如何得到结果”。交代关键数据、样本筛选、情景、假设、模型和稳健性逻辑。**截图原文公式，并解释其中每个符号、下标、单位及适用条件。** 原文未定义的符号不可杜撰，按上下文解释时标明解释性质。方法小节名优先沿用原文。

### 5 研究结果 Results

以原文结果的逻辑与**原文小节标题**组织；仅写各部分最主要的发现，保留必要数值、时间、方向和比较基准。**全部目标范围内的图与表都须截图，每张都须在结果正文中引用并说明主要发现。** 子图按原文引用，例如“……（图2a），……（图2b）”。

- 图：原文截图 → 中文图名 → 中文注释，三者均放图下。
- 表：中文表名 → 原文截图 → 中文注释；表名在截图上方，注释在截图下方。**表体不译、不重建。**
- 译全原有题注和注释，包括缩写、误差线、显著性、样本、颜色/符号及数据来源。
- 保留原文图表编号，勿因放置顺序改变编号。正文中的方法示意图、描述性统计表也纳入覆盖，放在首次被引用的位置附近。
- 长表跨页时分两段截图，第二段重复表头并标注“续表N”，仍用原编号；不缩放至不可读。
- 默认覆盖主文全部图表和公式。提供补充材料时，优先覆盖支撑主要结论的补充证据；只有用户明确要求补充材料全部图表时才逐一全收录。未提供的补充材料不得声称已读。

### 6 讨论 Discussion

原文有讨论时，按**原文讨论小节标题**逐节总结结论与推理链：作者如何解释、与已有认识如何衔接、边界在哪。不逐段翻译，不重复整段结果。原文讨论为连续段落、无子标题时，分享稿同样不加子标题，用“第一 / 第二……”的序号句承接。

### 7 结论或政策建议 Conclusions or policy implications

原文有独立结论或政策建议时提炼其主要判断，不重复结果数值。没有独立章节时，不虚构“作者结论”；可将讨论中的政策含义以“政策启示”呈现，或按用户要求省略本节。不得把自己的建议写成作者建议。

### 8 原文英文摘要 Original English abstract

直接复制原文英文摘要，完整且不改写。仅清除 PDF 提取造成的换行、断词或 OCR 错误，并与可见原文核对；不要把论文开头的引言并入摘要。非英文论文按原文实际提供的摘要处理。

可使用 [中文提纲](templates/share-outline.zh-CN.md)；[English outline](templates/share-outline.en.md) 用于理解相同结构，不改变默认中文交付。

## 不可省略的质量要求 Quality gates

- 以原文证据为准。Markdown 与 PDF 冲突时回看 PDF；不同位置的样本量、P 值、系数或编号冲突不得默默纠正。可在相关位置简短校注，区分原文记录、解释和未决疑点。
- 不将相关性写成因果，不将不显著写成无作用，不把对数点、百分比与百分点混用；核对分组结果与控制变量后的结论是否反转。
- 截图包括完整坐标轴、图例、子图标识、表格边缘（含表头与注释分隔线）和公式编号，保持纵横比与足够分辨率。太长时分段并保留续表/续图标记和原编号，不为塞入一页缩到不可读。
- Word 图文、题名和注释应相邻；公式后紧接符号解释。避免孤立标题、独占空页、裁切与重叠。
- 渲染最终 Word 并检查全部页面图像；修订后重新渲染。渲染不可用时诊断一次可用替代路径，并明确尚未完成视觉验收，不能宣称版式已核验。
- 本 skill 只授权当前任务的本地文档制作；不自动上传论文、训练案例、截图或成稿，不发送消息。GitHub 发布仅在用户明确要求时执行。

## English operating summary

Use paired source papers and prior DOCX summaries to learn editorial choices. Read the target paper in full, inventory all in-scope figures/tables/equations, and copy the original results/discussion subsection headings verbatim. Draft the eight sections above within the word budget, capture originals from the PDF — **tables as screenshots only, with the table body left untranslated and never rebuilt as native Word tables** — translate complete captions/notes, and cite every figure/table in the results narrative. Explain every equation symbol. Preserve the original English abstract. Distinguish source inconsistencies and author claims from inference. Render and inspect every final page before claiming layout verification. Scripts provide evidence and mechanical checks, not scientific or visual approval.
