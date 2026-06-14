title:: Asset Codes
alias:: four-letter asset code, Asset Code, asset code
public:: true

- All named concepts in this graph carry a **four-letter asset code** (sometimes five with a numeric suffix for instances).
- The convention is inherited from the [[Collibra Operating Model]] and extended with additional types.
- ## Collibra Core Asset Types (5)
  id:: collibra-core-types
	- | Code | Asset Type | Description |
	  | ---- | ---- | ---- |
	  | BTRM | Business Term | A defined term in the business vocabulary |
	  | BRUL | Business Rule | A rule governing data or process behaviour |
	  | DQRL | Data Quality Rule | A specific testable data quality constraint |
	  | DSET | Data Set | A named collection of data |
	  | ATTR | Attribute | A column or field within a Data Set |
- ## Extended Type Hierarchy
	- | Code | Asset Type | Parent | Description |
	  | ---- | ---- | ---- | ---- |
	  | AISYS | AI System | BTRM | A deployed AI system (see [[AI system]]) |
	  | AIMDL | AI Model | BTRM | An underlying AI model (see [[AI model]]) |
	  | SCEN | Scenario | BTRM | An event from AI's life (see [[Scenario]]) |
	  | PLCY | Policy | BRUL | A governance policy |
	  | SNSA | Sensitive Attribute | BTRM | A demographic or behavioural attribute carrying bias risk |
	  | BIAS | Bias Type | BTRM | A category of AI bias |
	  | UCAS | Use Case | BTRM | An AI use case with documented risk profile |
	  | RDAT | Reference Dataset | DSET | A canonical reference dataset |
	  | ENTT | Entity | BTRM | A top-level ontological entity in the type hierarchy |
	  | SAE | Self-Aware Entity | ENTT | An entity with capacity for self-awareness |
- ## Code Retrieval via Singine
	- Asset codes are managed in [[Singine]]. To retrieve or register a new code:
		- Codes follow the pattern `[A-Z]{4}(-[0-9]{3})?` — four uppercase letters, optionally followed by a hyphen and three-digit instance number.
		- New codes are proposed in pull requests by adding a row to this page and a corresponding page in the `pages/` directory.
		- The Singine platform validates uniqueness and maintains the canonical registry.
- ## File Transformation
	- To convert between Logseq Markdown, EDN, XML, or Collibra CSV formats, use [[SilkPage]] (`~/ws/silkpage`) or [[Singine]] (`~/ws/singine`).
