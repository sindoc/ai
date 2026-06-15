title:: AI as a Tool (Human-Controlled AI)
alias:: Human-Controlled AI, AI Tool
asset-code:: HAIR-T
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Artificial_intelligence
risk-tier:: Low

- **AI as a Tool** is the role in the [[Human-AI Relationships Glossary]] where an AI system functions as a passive instrument that executes precisely the commands given by a human operator, with no autonomous decision-making.
- ## Definition
	- In this role, the AI has no agency beyond its immediate instruction. It does not initiate actions, form goals, or deviate from its programmed function. The human retains full decision authority at every step.
	- This maps directly to the classic definition of AI as software that "enables machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving **defined goals**" — but in the Tool role, the goals are entirely human-defined and the scope is deliberately narrow.
	- Wikipedia describes [[Artificial intelligence]] as "the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making." In the Tool role, only the execution capability is delegated; judgement stays with the human.
- ## Characteristics
	- **Full human control** — the AI acts only when commanded
	- **Deterministic scope** — the task envelope is fixed at design time
	- **No persistent memory** across invocations (stateless by default)
	- **No goal formation** — the AI cannot modify its own objectives
	- **Transparent operation** — outputs are directly inspectable and auditable
- ## Risk Profile
	- **Risk tier**: Low
	- Risks remain present but are primarily attributable to the human operator:
		- Garbage-in / garbage-out from poor input quality
		- Misuse by the human directing the tool
		- Bias embedded in the training data that shaped tool behaviour
	- Governance burden falls on the human who deploys and directs the tool, not on the AI itself.
- ## Examples in Practice
	- A spell-checker suggesting corrections (human accepts or rejects each)
	- An image classifier labelling objects (human reviews labels)
	- A recommendation engine surfacing options (human chooses)
	- A translation API converting text (human validates output)
	- A code linter flagging issues (developer decides what to fix)
- ## Governance Markers
	- `asset-code:: HAIR-T`
	- Required disclosure: minimal — tool status is usually self-evident
	- Applicable policy: [[AI Governance/Policies/AI Use Case Documentation Policy]]
	- Bias check: inputs and training data must be audited; see [[AI Governance/Sensitive Attributes]]
- ## Code Sample
	- [[Code Samples/Python/Scenario Validator]] — validating scenario data contracts (AI-as-tool pattern)
- ## Wikipedia Context
	- [Artificial intelligence](https://en.wikipedia.org/wiki/Artificial_intelligence): "the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making."
- ## See Also
	- [[Human-AI Relationships Glossary]]
	- [[AI as an Assistant (Collaborative AI)]]
	- [[AI Risks]]
	- [[KnowYourAI]]
