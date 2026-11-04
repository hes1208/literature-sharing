# Installation and invocation

## 1. Portable use (no installation)

Keep the complete `literature-sharing` directory in an accessible location and ask the assistant to read its `SKILL.md` by absolute path. Preserve relative paths to `references`, `templates`, `scripts` and `examples`; copying only the entry file breaks those links. Reading the instructions needs no Python — only the utility scripts do.

```text
Read /path/to/literature-sharing/SKILL.md and follow it for this task.
Paper Markdown: ...; paper PDF: ...; save the DOCX to: ...
```

## 2. WorkBuddy (verified path)

### 2.1 Put the folder under the user-level skills directory

On Windows the user-level directory is `%USERPROFILE%\.workbuddy\skills\`. Keep the folder name `literature-sharing`, with `SKILL.md` at its root:

```text
C:\Users\<you>\.workbuddy\skills\literature-sharing\SKILL.md
```

PowerShell, runtime files only:

```powershell
$src = "D:\path\to\literature-sharing"
$dst = "$env:USERPROFILE\.workbuddy\skills\literature-sharing"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
foreach ($d in "agents","references","templates","scripts","examples") {
    Copy-Item -Recurse -Force (Join-Path $src $d) $dst
}
Copy-Item -Force (Join-Path $src "SKILL.md"), (Join-Path $src "requirements.txt"), (Join-Path $src "LICENSE") $dst
```

`README`, `.github`, `tests` and `docs` are repository-facing and optional at runtime.

### 2.2 When it takes effect

Start a **new session**. The skill appears as “文献分享 Literature Sharing” in the skills panel once loaded. One extra nested folder is enough to break discovery.

### 2.3 Daily invocation

Three equivalent ways:

- **By name**: `Use $literature-sharing to summarise this paper...`
- **By natural language**: `Turn this paper into a Chinese journal-club Word document` — the description already contains 文献分享 / 论文分享稿 trigger terms, so the skill loads automatically.
- **From the skills panel**: open a conversation from the skill entry.

### 2.4 Copy-paste prompt template

```text
Use $literature-sharing to produce a Chinese share document.

Paper Markdown: D:\...\paper.md
Paper PDF: D:\...\paper.pdf
Paired examples (optional): D:\...\examples
Output directory: D:\...\out

Requirements:
1. Tables as screenshots only — do not translate the table body, do not rebuild tables in Word.
2. Translate the original Results/Discussion subheadings one-to-one; add or drop none.
3. Keep prose inside the push-length budget (background 300–450 characters, results 800–1200).
4. Include every figure and table and cite each one in the prose with its key numbers.
5. Render and inspect every final page before delivery.
```

These five requirements restate the hard conventions in `SKILL.md`; omitting them still applies the defaults, but stating them removes back-and-forth.

### 2.5 Markdown-only or PDF-only

- **Markdown only**: textual analysis is possible, but the assistant must not claim the original screenshots and layout were verified.
- **PDF only**: convert with MinerU first, as recommended in `SKILL.md`; keep the PDF for screenshots.

## 3. Codex and other hosts supporting local skills

Copy the folder into the configured skills directory, keeping the name `literature-sharing`. The usual default is `~/.codex/skills`; use the actual configuration when it differs:

```text
~/.codex/skills/literature-sharing/SKILL.md
```

Reload skills or start a new session, then invoke `$literature-sharing`. Discovery is host- and version-dependent; a copied folder alone does not prove successful loading.

## 4. Utility environment

Python 3.10+, preferably the host's supplied runtime. Otherwise:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

macOS / Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

These steps prepare only the utility scripts (PDF cropping, DOCX coverage checks). They do not install Word or a DOCX renderer; visual verification still requires host-provided document tools.

## 5. Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| Skill not listed | `SKILL.md` is not at `skills/literature-sharing/` root, or the session was not restarted |
| Figures look blurry or carry URLs | Remote Markdown images were used; re-capture from the PDF |
| Tables came back translated | Screenshot rule not applied; restate “tables as screenshots, body untranslated” |
| Output too long | Give a target length, or ask for a rewrite against the word budget |
| Subheadings do not match the paper | Ask for a one-to-one pass against the source `Results` / `Discussion` headings |

GitHub publishing is a separate operation; see [WORKBUDDY_HANDOFF.md](WORKBUDDY_HANDOFF.md).
