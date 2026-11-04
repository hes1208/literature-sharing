# 工具指南 Utility guide

## PDF截图 / PDF screenshots

先把页面渲染成图片并查看，再决定矩形范围。页码从1开始；坐标为渲染后页面左上角原点的 point，不是像素。1 point = 1/72英寸，默认300 DPI。

Render and inspect whole pages first. Page numbers are 1-based. Crop boxes use displayed-page top-left points, not pixels. The script does not locate figures automatically.

```bash
python scripts/pdf_assets.py --pdf work/paper.pdf --out-dir work/pages --render-pages 1 2 3
python scripts/pdf_assets.py --pdf work/paper.pdf --plan work/crop-plan.json --out-dir work/assets --dpi 300
```

方案格式参见 [模拟示例](../examples/crop-plan.example.json)。`bbox` 为 `[left, top, right, bottom]`，必须处于显示页面范围内，`id` 必须唯一且仅含字母、数字、下划线或连字符。`--plan` 与 `--render-pages` 可同时使用。输出包含PNG及 `assets-manifest.json`，记录原PDF文件名、SHA-256、页码、坐标和DPI。

Plan format: see the [synthetic example](../examples/crop-plan.example.json). IDs are unique safe filenames. The manifest records source filename/hash and crop provenance. Existing files with matching generated names are overwritten; use a fresh task output directory. The source PDF is never edited.

脚本校验矩形和页码，但无法判断图例是否已被裁掉。每张截图都必须查看。旋转页面的范围以实际渲染方向为准。

## Word覆盖检查 / DOCX coverage checks

按论文实际清单填写台账，路径相对于台账文件。例如台账位于 `work/evidence-ledger.json`，截图字段为 `assets/fig1.png`，则截图应位于 `work/assets/fig1.png`。

```bash
python scripts/check_share.py --docx outputs/share.docx --ledger work/evidence-ledger.json --abstract-file work/abstract.txt --report work/check.json
python scripts/check_share.py --docx outputs/share.docx --ledger work/evidence-ledger.json --max-body-chars 4200
```

台账格式参见 [模拟示例](../examples/evidence-ledger.example.json)。论文若无讨论或政策内容，不要求生成相应章节；`sections` 只填写该论文实际需要检查的章节。`number` 使用字符串以支持 `S1` 等编号。

`caption` 必须与成稿中的完整题名/公式标签对应；`citation` 填写独立正文段落中出现的准确引用片段，如 `图1` 或 `（图1a）`。`symbols` 填写解释文字中实际使用的每个符号，人工核对其含义。

报告中的 `native_tables` 统计 Word 原生表格对象数。表格按规则应为截图，该值大于 0 时脚本给出提醒，需人工确认它只是版式用表或已在注释中声明的补充材料重排表。`body_cjk_chars` 为正文汉字数的近似值（已排除以“图/表/注”开头及题注式段落），配合 `--max-body-chars` 可在超出篇幅预算时提醒。

The checker verifies the six metadata fields, basic Chinese section keywords, sections required by the ledger, screenshot file existence, expected captions, independent narrative citations and presence of equation symbols in editable text. An optional UTF-8 abstract file is matched after Unicode NFC and whitespace normalization; punctuation and wording remain significant.

退出码 / Exit codes:

- `0`：机械检查无错误 / No mechanical errors.
- `1`：发现内容覆盖错误 / Coverage or abstract mismatch.
- `2`：输入/格式/文件读取错误 / Invalid or unreadable input.

**局限 / Limitations:**

- 仅检查正文普通段落和行内图片统计，不解析文本框、表格单元格、浮动图形或图内英文。
- 检查图片数量只是提示，不证明Word里插入的是对应来源截图。
- 台账遗漏的对象不会被脚本自动发现，必须先与原文逐项核对完整清单。
- 题注存在不代表译全，符号出现不代表解释正确。
- 不能验证结论、统计解释、完整题注、位置、分页、清晰度或视觉缺陷。
- `ok: true` 只说明机械检查通过，不能替代人工/助手学术核对与逐页渲染检查。

## 验证工具本身 / Testing the utilities

```bash
python -m unittest discover -s tests -v
```

测试动态生成模拟PDF和DOCX，验证裁剪尺寸与颜色、来源哈希、无效坐标与文件名拒绝、题注不冒充正文引用、摘要匹配、原生表格与篇幅提醒。不会读取真实论文，不需要联网或Office。

Tests generate synthetic PDF/DOCX fixtures locally. They do not certify the scientific quality of documents created with this skill or compatibility with every assistant.
