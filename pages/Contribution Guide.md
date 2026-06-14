title:: Contribution Guide
public:: true

- ## How Contributions Work
	- Fork the `ai` repository, make your changes on a branch, and open a pull request.
	- Every PR must add or amend at least one [[Scenario]] page.
	- All scenarios must involve **at least two AI systems**, or one AI system interacting with a human in a governance-relevant way.
- ## Scenario Naming Convention
	- Page name: `Scenario/<namespace>/<id>___<short-title>`
	- File name: `Scenario___<namespace>___<id>___<short-title>.md` (Logseq triple-lowbar convention)
	- `<id>` is a zero-padded three-digit number: `001`, `002`, etc.
	- Namespaces: `Multi-AI`, `Human-AI`, `Governance`, `Edge`
- ## Mandatory Fields (in page properties)
	- `asset-code::` — `SCEN-<id>` (see [[Asset Codes]])
	- `public:: true`
- ## Asset Code Registration
	- To register a new asset type (not just a new scenario instance), add a row to [[Asset Codes]] in the same PR.
	- Codes follow `[A-Z]{4}` — four uppercase letters, unique across the graph.
- ## File Formats
	- Pages: Logseq Markdown (`.md`) with triple-lowbar `___` for namespace separators in filenames.
	- Config: EDN at `logseq/config.edn`.
	- To convert to Collibra CSV, XML, or EDN: use [[SilkPage]] (`~/ws/silkpage`) or [[Singine]] (`~/ws/singine`).
- ## Review Criteria
	- At least one reviewer must verify:
		- [ ] Minimum two AI systems named (or valid Human-AI scenario)
		- [ ] Risk profile linked via [[Human-AI Relationships Glossary]]
		- [ ] No sensitive attribute handling without a flag in [[AI Governance___Sensitive Attributes]]
		- [ ] Asset code registered or reused correctly
