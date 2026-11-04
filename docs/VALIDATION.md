# 本地验证记录 Local validation

验证日期 / Date: 2026-11-04（v0.2.0）

| 项目 / Item | 结果 / Result |
| --- | --- |
| 官方 skill-creator `quick_validate.py` | 通过 / Passed |
| 入口名称与frontmatter | 通过 / Passed |
| JSON示例解析 | 通过 / Passed |
| YAML元数据、协作模板与工作流解析 | 通过 / Passed |
| Markdown相对链接 | 无失效目标 / No missing targets |
| 5项模拟脚本测试 | 全部通过 / All passed |
| 本地操作系统与Python | Windows, Python 3.12 |

模拟测试覆盖：PDF坐标及裁剪像素尺寸、颜色与来源SHA-256；非法文件名、页码和矩形拒绝；Word覆盖与摘要一致性；题注不能代替独立结果引用；Word原生表格计数与正文字数预算提醒。

Synthetic tests cover crop geometry, pixel color and provenance hash; invalid IDs/pages/rectangles; DOCX coverage and abstract matching; caption-versus-narrative citation distinction; and native-table / body-length signals.

## 端到端实践 / End-to-end run

v0.2.0 的三条硬性惯例来自一次完整的真实交付：一篇 Nature 系列研究论文（5 幅多子图、4 张表、6 个公式），以 12 份既有分享稿为案例学习样本，产出 13 页中文 Word 分享稿，并逐页渲染验收。

该次交付暴露并已在 v0.2.0 中固化为规则的问题：

1. 曾把 4 张表重建为中英对照的 Word 原生表格 —— 违反“表格只截图”，并带来数值抄录与结构失真风险。
2. 曾自造结果小节标题（新增原文没有的“数据覆盖结构”一节，并改写其余小节措辞）—— 违反“标题忠实原文”。
3. 背景约 900 字、结果约 1600 字 —— 超出公众号推送的可读长度，需按预算压缩。

The three hard conventions in v0.2.0 come from a full real delivery. That run exposed exactly the three failures now codified as rules: rebuilt tables, invented result subheadings, and over-long background/results prose.

## 未验证项 / Not verified

GitHub 远端 CI、WorkBuddy 自动导入、全部宿主与操作系统组合，以及非 Windows 环境下的 DOCX 渲染路径。辅助脚本通过不代表科学内容或最终 Word 视觉排版已通过。

Not verified: remote GitHub CI, automatic WorkBuddy import, every host/OS combination, and DOCX rendering outside Windows. Utility tests do not certify scientific content or final DOCX layout.
