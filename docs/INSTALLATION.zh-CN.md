# 安装与调用

## 一、最快的方式：让助手直接读取入口文件

不安装也能用。把整个 `literature-sharing` 目录放在助手可访问的位置，给出 `SKILL.md` 的绝对路径：

```text
请先读取 D:\path\to\literature-sharing\SKILL.md，再按其中流程完成本次文献分享。
论文 Markdown：……；论文 PDF：……；成稿保存到：……。
```

保留 `references`、`templates`、`scripts`、`examples` 的相对位置；只复制入口文件会丢失关联资料。纯指令使用无需 Python，只有跑辅助脚本时才需要依赖。

## 二、WorkBuddy（本机实测路径）

### 1. 放入用户级技能目录

Windows 用户级目录为 `%USERPROFILE%\.workbuddy\skills\`，目录名保持 `literature-sharing`，`SKILL.md` 位于该目录根层：

```text
C:\Users\<你的用户名>\.workbuddy\skills\literature-sharing\SKILL.md
```

PowerShell 复制命令（只带必要文件）：

```powershell
$src = "D:\path\to\literature-sharing"
$dst = "$env:USERPROFILE\.workbuddy\skills\literature-sharing"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
foreach ($d in "agents","references","templates","scripts","examples") {
    Copy-Item -Recurse -Force (Join-Path $src $d) $dst
}
Copy-Item -Force (Join-Path $src "SKILL.md"), (Join-Path $src "requirements.txt"), (Join-Path $src "LICENSE") $dst
```

`README`、`.github`、`tests`、`docs` 属于仓库展示内容，可不复制。

### 2. 何时生效

放入后需**新开一个会话**；侧边栏「技能」列表中出现「文献分享 Literature Sharing」即已加载。目录层级错一层（例如多套了一层文件夹）会导致识别失败。

### 3. 日常调用

三种方式，效果相同：

- **显式点名**：`用 $literature-sharing 做这篇论文的分享稿……`
- **自然语言触发**：`把这篇文章做成中文文献分享 Word`——技能描述里已包含“文献分享”“论文分享稿”等触发词，助手会自动加载。
- **侧边栏**：在「技能」中找到该技能后开启对话。

### 4. 可直接复制的调用模板

```text
用 $literature-sharing 做这篇论文的中文分享稿。

论文 Markdown：D:\...\paper.md
论文 PDF：D:\...\paper.pdf
案例目录（可选）：D:\...\训练集-案例
输出目录：D:\...\分析集

要求：
1. 表只截图，不要翻译表体，也不要重建为 Word 表格；
2. 结果和讨论的小标题照原文逐条翻译，不增不减；
3. 正文按公众号推送长度控制（背景 300–450 字，结果 800–1200 字）；
4. 图和表全部收录，并在正文中逐张引用、给出关键数值；
5. 交付前逐页渲染检查排版。
```

模板里的五条要求与 `SKILL.md` 的硬性惯例一致，写上可减少来回确认；不写也会按默认规则执行。

### 5. 只有 Markdown 或只有 PDF 时

- 只有 Markdown：可完成文字分析，但**不能声称已完成原文截图与版面核验**，助手应明确告知这一缺口。
- 只有 PDF：先按 `SKILL.md` 的建议用 MinerU 转成 Markdown，再分析；PDF 始终保留用于截图。

## 三、Codex 等支持本地 skill 的环境

将目录放入配置的技能目录，目录名保持 `literature-sharing`，默认通常为 `~/.codex/skills`，以实际配置为准：

```text
~/.codex/skills/literature-sharing/SKILL.md
```

重新加载技能或开启新会话，再使用 `$literature-sharing`。技能是否在界面中显示取决于宿主与版本，复制成功不等于已加载。

## 四、辅助脚本环境

Python 3.10+。若助手提供统一运行时，优先使用该运行时；否则在仓库目录建立虚拟环境：

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS / Linux：

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

以上命令只准备辅助脚本（PDF 裁剪、Word 覆盖检查），不安装 Word 或 DOCX 渲染器；最终视觉验收需宿主已有的文字处理或渲染能力。

## 五、常见问题

| 现象 | 原因与处理 |
| --- | --- |
| 技能列表里找不到 | 检查 `SKILL.md` 是否在 `skills/literature-sharing/` 根层；改完需新开会话 |
| 正文有了，但图是模糊的或带网址 | 直接用了 Markdown 里的远程图片；必须回 PDF 截图 |
| 表格被翻成中文 | 未采用截图规则；在请求中重申“表只截图，不译表体” |
| 篇幅过长 | 指出目标字数，或让助手按 `SKILL.md` 的篇幅预算重写背景与结果 |
| 小标题与原文对不上 | 要求逐条对照原文 `Results` / `Discussion` 子标题重新拟题 |

GitHub 上传是单独操作，见 [交接说明](WORKBUDDY_HANDOFF.md)。读取技能不会自动授权上传论文或目录外材料。
