# ai

A community knowledge graph documenting **scenarios from AI's life** — interactions and events in which AI systems are the primary actors.

## Philosophy

Every contribution proposes a real or plausible scenario in which **at least two AI systems** are involved: interacting with each other, with a human, or with the world in a way that raises governance or philosophical questions worth studying.

The graph is maintained in [Logseq](https://logseq.com/) and open to pull requests.

## How to Contribute

1. Fork this repository.
2. Add a new page under `pages/Scenario___<namespace>___<id>___<title>.md` (follow the `Scenario/Template` page).
3. Open a pull request — one scenario per PR is preferred.

See `pages/Contribution Guide.md` for naming conventions, mandatory page properties, and review criteria.

## Opening in Logseq

Point Logseq at this directory (`~/ws/ai`) as a new graph. The home page is **AI Life**.

## Foundational Model

This graph is seeded from the [SinDoc Public Graph](https://sindoc.github.io/website/), which covers Data & AI Governance, the KnowYourAI framework, and reference data. The asset model is compatible with the [Collibra](https://www.collibra.com/) operating model, extended with a custom type hierarchy using four-letter codes (see `pages/Asset Codes.md`).

## File Transformations

To convert between Logseq Markdown, EDN, XML, and Collibra CSV:
- **SilkPage**: `~/ws/silkpage`
- **Singine**: `~/ws/singine`
