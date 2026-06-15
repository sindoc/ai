title:: AI as a Manager (AI-Led Decision Making)
alias:: AI-Led Decision Making, AI Manager
asset-code:: HAIR-M
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Artificial_intelligence
risk-tier:: High

- **AI as a Manager** is the role in the [[Human-AI Relationships Glossary]] where an AI system makes substantive decisions and humans carry out those decisions or provide oversight, rather than the other way around.
- ## Definition
	- In the manager role, the flow of authority is inverted compared to the tool and assistant roles: the AI defines what should be done, and humans execute, monitor, or review. Human involvement does not disappear, but it shifts from directing to supervising.
	- This role encompasses systems that allocate work (gig-economy routing algorithms), set prices (dynamic pricing engines), score individuals (credit scoring, fraud detection, hiring screeners), or recommend interventions (predictive policing, content moderation queues).
	- The risk profile is High because consequential decisions about real people are made at machine speed and scale, often without meaningful human review of individual cases.
- ## Characteristics
	- **Decision authority delegated to AI** — the AI's output is the decision, not input to a human decision
	- **Human supervision at aggregate level** — humans review statistics, edge cases, and policy parameters, not individual cases
	- **High throughput** — operates at scale and speed beyond human review capacity
	- **Feedback loops** — the AI's decisions shape the environment from which it learns, creating reinforcement dynamics
	- **Opacity risk** — decision logic may be opaque to the humans nominally in charge
- ## Risk Profile
	- **Risk tier**: High
	- Key risks in the manager role:
		- **Accountability vacuum** — when the AI decides, no human can be directly held responsible for each outcome
		- **Disparate impact** — AI managers operating at scale can produce systematic discrimination faster and more consistently than human managers
		- **Audit complexity** — auditing millions of AI decisions requires specialised tooling (see [[AI Governance/Tools/NannyML]])
		- **[[Human Value Drift]]** — organisational values shift to accommodate what the AI optimises for, not the other way around
		- **Regulatory exposure** — EU AI Act, CCPA, and sector regulations (FCRA, ECOA) impose specific requirements on automated decision-making affecting individuals
	- High-risk scenarios involving the manager role require mandatory [[AI Governance/Policies/AI Use Case Documentation Policy]] registration and third-party audit trail.
- ## Examples in Practice
	- A content moderation queue where AI flags and an AI decides; human only reviews escalations
	- An algorithmic trading system executing buy/sell orders within policy guardrails set by humans
	- A hiring screener ranking and rejecting applications before any human sees them
	- A dynamic pricing engine setting prices minute-by-minute without human approval
	- An AI scheduling tool assigning shifts and work queues to human workers
- ## Governance Markers
	- `asset-code:: HAIR-M`
	- Required: impact assessment for any deployment affecting individuals' access to services, credit, employment, or liberty
	- Required: human review mechanism for contested decisions (right to explanation and appeal)
	- Required: bias audit at deployment and on a regular cadence
	- Applicable policy: [[AI Governance/Policies/AI Use Case Documentation Policy]], [[AI Governance/Policies/AI Monitoring Policy]]
- ## Wikipedia Context
	- [AI safety](https://en.wikipedia.org/wiki/AI_safety): "an interdisciplinary field focused on preventing accidents, misuse, or other harmful consequences arising from artificial intelligence systems."
	- [AI alignment](https://en.wikipedia.org/wiki/AI_alignment): "alignment aims to steer AI systems toward a person's or group's intended goals, preferences, or ethical principles."
- ## See Also
	- [[Human-AI Relationships Glossary]]
	- [[AI as an Augmenter (Human-AI Symbiosis)]]
	- [[AI as an Autonomous Agent (AI Independence)]]
	- [[AI Risks]]
	- [[AI Governance]]
	- [[KnowYourAI]]
