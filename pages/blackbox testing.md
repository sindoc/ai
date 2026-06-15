title:: blackbox testing
alias:: Black-box Testing, black box testing, specification-based testing
asset-code:: BBTST
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Black-box_testing

- **Black-box testing** (also written *blackbox testing*) is a method of software and AI evaluation that assesses a system's outputs and behaviour without access to or knowledge of its internal structure.
- Wikipedia: "a method of software testing that examines the functionality of an application without peering into its internal structures or workings. This method of test can be applied virtually to every level of software testing: unit, integration, system and acceptance."
- ## Significance for AI Systems
	- Most production [[Large Language Model]]s and AI systems are black boxes: their internal weights, activation patterns, and decision paths are not directly observable by users or auditors.
	- Black-box evaluation techniques for AI include:
		- **Prompt probing** — systematically varying inputs to characterise output distributions
		- **Red-teaming** — adversarial input testing to find failure modes
		- **Behavioural consistency testing** — checking that semantically equivalent prompts yield consistent responses
		- **Output auditing** — statistical analysis of model outputs across demographic groups (see [[AI Governance/Sensitive Attributes]])
- ## In This Knowledge Graph
	- Scenario submissions should include blackbox test cases where feasible: a set of inputs and expected output characteristics that can be re-run to verify governance compliance.
	- See [[AI Governance/Tools/NannyML]] for drift-aware monitoring in production.
- ## See Also
	- [[AI system]]
	- [[AI Governance]]
	- [[AI Risks]]
