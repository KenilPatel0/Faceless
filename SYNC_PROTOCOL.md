# 🔄 Dual-Space Synchronization Protocol & Architecture Guide

> **Master Architecture Specification for Maintainers & AI Agents**  
> This document defines how improvements to motion graphics, video rendering, agent skills, and production rules are synchronized between the **Public Open-Source Framework** and the **Private Creator Workspace (`TechXKenil/`)** without risking private channel data leaks.

---

## 1. Dual-Space Architectural Model

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   FACLESS VIDEO ENGINE REPOSITORY                      │
├───────────────────────────────────┬────────────────────────────────────┤
│   🌐 PUBLIC OPEN-SOURCE SPACE     │    🔒 PRIVATE CREATOR WORKSPACE    │
│       (Committed to GitHub)       │        (Excluded in .gitignore)    │
├───────────────────────────────────┼────────────────────────────────────┤
│ • agents/skills/                  │ • TechXKenil/skills/               │
│   ├── motion-editing/             │   ├── techxkenil-motion-editing/   │
│   ├── humanized-video/            │   ├── techxkenil-humanized-video/  │
│   └── real-ui/                    │   └── techxkenil-real-ui/          │
│ • agents/rules/                   │ • TechXKenil/rules/                │
│   └── video-production-rules.md   │   ├── video-production-rules.md    │
│ • tools/                          │   └── techxkenil-video-rules.md    │
│   ├── channel_config.py           │ • TechXKenil/channel_profile.json  │
│   ├── motion.py                   │ • TechXKenil/GEMINI.md             │
│   ├── humanize.py                 │ • TechXKenil/docs/                 │
│   └── sync_engine.py              │   ├── IDEAS.md (Private Roadmap)   │
│ • templates/ & channel.example.json│   └── brand.md                     │
│ • GEMINI.md (Public Instructions) │ • VideoFiles/ (Local Video Suites) │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 2. Strictly Protected Private Assets (Zero-Leak List)

The following files contain private channel intellectual property and **must NEVER be synced, renamed, or committed to GitHub**:

| File / Folder | Purpose | Privacy Enforcement |
|---|---|---|
| **`TechXKenil/docs/IDEAS.md`** | Kenil's unpublished video roadmap & backlog | Protected by `.gitignore` & `sync_engine.py` |
| **`TechXKenil/channel_profile.json`**| Personal channel config & voice profile | Protected by `.gitignore` |
| **`TechXKenil/`** (Entire folder) | Private creator workspace | Listed in `.gitignore` |
| **`VideoFiles/*/`** | Local video projects, WAVs, MP4s, frames | Excluded in `.gitignore` |
| **`channel.json`** | User's local active channel profile | Excluded in `.gitignore` |

---

## 3. The 4-Step Improvement & Sync Workflow

Whenever an enhancement is made to video animations, subtitle safe areas, rendering physics, or agent skills, execute this exact workflow:

### Step 1: Implement the Enhancement
Update the primary code, skill, or rule:
- Code enhancements: `tools/motion.py`, `tools/humanize.py`, `tools/qa.py`, `tools/channel_config.py`.
- Skill enhancements: `agents/skills/motion-editing/`, `agents/skills/humanized-video/`, etc.
- Master instructions: `GEMINI.md` and `agents/rules/video-production-rules.md`.

### Step 2: Run Automated Dual-Space Sync
Execute the synchronization engine to propagate the improvements into `TechXKenil/` with automatic branding adaptation:
```bash
python tools/sync_engine.py sync
```
This updates `TechXKenil/skills/` and `TechXKenil/rules/` while preserving Kenil's personal channel branding and protecting private files.

### Step 3: Run Security & Leak Verification
Verify that zero private files are tracked and `.gitignore` remains intact:
```bash
python tools/sync_engine.py verify
```
This performs 4 automated checks:
1. `.gitignore` explicitly excludes `TechXKenil/` and `channel.json`.
2. `git status` contains zero files from `TechXKenil/`.
3. Private assets (`IDEAS.md`, `channel_profile.json`) remain safely untouched.
4. `tools/channel_config.py` correctly resolves the active channel identity.

### Step 4: Commit & Push Public Framework
```bash
git add -A
git commit -m "feat: [describe enhancement]"
git push origin main
```

---

## 4. Automation CLI: `tools/sync_engine.py`

| Command | Action |
|---|---|
| `python tools/sync_engine.py status` | Inspects drift and shows side-by-side synchronization status. |
| `python tools/sync_engine.py sync` | Propagates shared improvements between public and private spaces. |
| `python tools/sync_engine.py verify` | Strict leak detector (verifies `.gitignore`, git index, and private files). |

---

## 5. Agent Instructions (Antigravity Mandate)
Whenever the user asks to **improve skills**, **update rules**, or **enhance video production**, the agent must:
1. Apply the improvements to both the **public framework** (`agents/skills`, `agents/rules`, `tools/`) and **Kenil's workspace** (`TechXKenil/`).
2. Run `python tools/sync_engine.py verify` to guarantee zero private leaks.
3. Keep the public repository 100% white-labeled and generic while keeping Kenil's channel profile fully active locally.
