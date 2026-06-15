# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository is a **Logseq knowledge graph** about scenarios from AI's life. It is community-editable via pull requests. Every contribution must involve at least two AI systems interacting, or one AI system interacting with a human in a governance-relevant way.

The canonical entry point when working in this graph is `pages/AI Life.md`.

## Repository Structure

```
ai/
├── pages/          # All knowledge graph pages (Logseq Markdown, triple-lowbar filenames)
│   ├── AI Life.md               # Homepage / entry point
│   ├── Scenario.md              # Core concept: what a scenario is
│   ├── Scenario___Template.md   # PR template for new scenarios
│   ├── Scenario___Multi-AI___*  # Scenarios involving ≥2 AI systems
│   ├── Scenario___Human-AI___*  # Scenarios involving one AI + human(s)
│   ├── Asset Codes.md           # Four-letter code registry (Collibra-compatible)
│   ├── Collibra Operating Model.md
│   ├── Human-AI Relationships Glossary.md
│   ├── AI Governance*.md        # Governance, policies, bias, tests, tools
│   ├── Data & AI Governance.md
│   ├── KnowYourAI.md
│   ├── Contribution Guide.md
│   ├── SilkPage.md
│   └── Singine.md
├── logseq/
│   └── config.edn               # Logseq graph config (home page, favorites, file format)
├── journals/                    # Logseq journals (date-stamped notes)
├── assets/                      # Binary assets referenced in pages
└── README.md
```

## Logseq Filename Convention

Logseq uses **triple-lowbar** (`___`) for namespace separators in filenames. A page titled `Scenario/Multi-AI/001/Two LLMs Debate a Policy` is stored as:

```
pages/Scenario___Multi-AI___001___Two LLMs Debate a Policy.md
```

Page properties go at the top of the file as `key:: value` (Logseq property syntax), not YAML frontmatter.

## Asset Code Convention

All named concepts carry a **four-letter asset code** in their `asset-code::` property. The registry lives in `pages/Asset Codes.md`.

- Core Collibra codes: `BTRM`, `BRUL`, `DQRL`, `DSET`, `ATTR`
- Extended codes in this graph: `AISYS`, `AIMDL`, `SCEN`, `PLCY`, `SNSA`, `BIAS`, `UCAS`, `RDAT`, `ENTT`, `SAE`, `LLMD`, `HAIR`, `DAIG`, `AIGOV`
- Scenario instances use `SCEN-<nnn>` (e.g. `SCEN-001`)
- New asset types go in `Asset Codes.md` as part of the same PR that introduces them
- Code validation and uniqueness registry: `~/ws/singine`

## Scenario Page Structure

Every scenario page must include:

```markdown
asset-code:: SCEN-<nnn>
public:: true

- **ID**: `SCEN-<nnn>`
  **Namespace**: `Scenario/<type>`
- ### Participants
  (at least two AI systems named with their model providers)
- ### Description
- ### Interaction Log or Link
- ### Governance Considerations
  (risk profile linked via Human-AI Relationships Glossary)
- ### Why This Belongs in AI's Life
```

See `pages/Scenario___Template.md` for the full template.

## Human-AI Relationships Glossary (Risk Tiers)

Scenarios must link to one of these five roles from `pages/Human-AI Relationships Glossary.md` to inherit a risk profile:

| Term | Risk |
|------|------|
| AI as a Tool (Human-Controlled AI) | Low |
| AI as an Assistant (Collaborative AI) | Medium |
| AI as an Augmenter (Human-AI Symbiosis) | Medium |
| AI as a Manager (AI-Led Decision Making) | High |
| AI as an Autonomous Agent (AI Independence) | High |

High-risk scenarios require additional review.

## File Transformation

To convert between Logseq Markdown, EDN, XML, or Collibra CSV:
- **SilkPage**: `~/ws/silkpage/main`
- **Singine**: `~/ws/singine/src/`

Both tools are available locally. Use them when a contributor submits assets in a non-Markdown format, or when exporting the graph for Collibra import.

## Key Cross-Repo Relationships

| Repo | Role |
|------|------|
| `~/ws/singine` | Asset code registry; subscriber/import pipeline |
| `~/ws/silkpage` | File transformation (Markdown ↔ EDN ↔ XML ↔ Collibra CSV) |
| `~/ws/ls/public/main/website` | Source public graph this repo was seeded from |
| `~/ws/ls/kern` | Private Logseq graph (journals and private pages) |

## Development Commands

### First-time remote setup

```bash
# Create the GitHub repo (requires gh CLI)
gh repo create sindoc/ai --public --source=. --remote=origin --push

# Or manually: create at github.com/new, then:
git remote add origin git@github.com:sindoc/ai.git
git push -u origin main
```

### Contribute a branch + PR

```bash
git checkout -b feat/my-change
# ... make changes ...
git add pages/Scenario___My-New-Scenario.md
git commit -m "feat: add SCEN-006 ..."
git push -u origin feat/my-change
gh pr create --title "feat: ..." --body "..."
```

### Submodule init (after cloning)

```bash
git submodule update --init --recursive
```

## Opening in Logseq

Point Logseq at `~/ws/ai` as a new graph. The configured home page is **AI Life**. Logseq must be used (not just a text editor) to validate that page links resolve and the graph renders correctly before merging a PR.
