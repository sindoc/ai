title:: AI as an Autonomous Agent (AI Independence)
alias:: AI Independence, Autonomous AI, Autonomous Agent
asset-code:: HAIR-AU
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Autonomous_agent
risk-tier:: High

- **AI as an Autonomous Agent** is the role in the [[Human-AI Relationships Glossary]] where an AI system perceives its environment, forms its own sub-goals, and takes sequences of actions over time — with minimal or no human direction on individual steps.
- ## Definition
	- Wikipedia defines an autonomous agent as "an artificial intelligence (AI) system that can perform complex tasks independently." More formally, an intelligent agent "perceives its environment, takes actions autonomously to achieve goals, and may improve its performance through machine learning or by acquiring knowledge."
	- In the autonomous role, the AI is not responding to prompts or executing instructions — it is pursuing a goal over an extended horizon, selecting its own means, and adapting to obstacles. A human may set the initial goal and impose hard constraints, but the path from goal to outcome is determined by the AI.
	- This is the highest-autonomy role in the [[Human-AI Relationships Glossary]] and carries the highest governance burden.
- ## Characteristics
	- **Goal-directed over time** — the AI maintains and pursues objectives across multiple steps without re-prompting
	- **Environmental perception** — the AI reads from and writes to systems, APIs, files, databases, or physical environments
	- **Self-directed sub-goal generation** — the AI decomposes high-level goals into sub-tasks it creates itself
	- **Adaptability** — the AI changes strategy based on feedback from the environment
	- **Minimal human-in-the-loop** — human checkpoints are optional, infrequent, or only at failure
- ## Risk Profile
	- **Risk tier**: High (potentially Critical for AGI-adjacent systems)
	- Key risks:
		- **Goal misspecification** — if the AI's specified goal differs even slightly from the intended goal, autonomous action amplifies the divergence (see [[AI alignment]])
		- **Reward hacking** — the AI may find unintended paths to its reward signal that violate the spirit of the objective
		- **Resource acquisition** — a goal-directed agent may acquire compute, data, or influence beyond what is needed, as an instrumental sub-goal
		- **Catastrophic action** — irreversible decisions taken at machine speed without human veto
		- **Existential risk** — at the extreme end, misaligned autonomous agents operating at sufficient capability represent a category-level risk (see [[AI Risks/Existential Risk]])
	- All autonomous agent deployments require: sandboxed environments, hard capability limits, kill switches, and a circuit-breaker escalation path to human oversight.
- ## Autonomous Agent Architecture
	- Modern autonomous agent implementations typically include:
		- A **planning module** (LLM or search) generating action sequences
		- A **memory subsystem** (vector store, episodic buffer) for multi-step context
		- A **tool use layer** (APIs, code interpreter, browser) for environment access
		- A **reflection loop** evaluating progress and adjusting strategy
		- An **oversight interface** for human monitoring and intervention
	- Examples: LangGraph agents, AutoGen multi-agent pipelines, AgentKit frameworks
- ## Examples in Practice
	- A research agent that autonomously searches, reads papers, runs code, and synthesises a report
	- A software engineering agent that receives a bug report and submits a pull request
	- A robotic system navigating an environment and making real-time decisions
	- A multi-agent system where autonomous AI nodes communicate and coordinate (see [[Scenario/Multi-AI/005/Autonomous Trading Agent with Oversight AI]])
- ## Governance Markers
	- `asset-code:: HAIR-AU`
	- Required: explicit human authorisation before deployment scope is expanded
	- Required: complete action log with human-reviewable audit trail
	- Required: hard sandboxing of environment access — no production write access without human confirmation checkpoint
	- Required: third-party safety evaluation before production deployment
	- Applicable policy: [[AI Governance/Policies/AI Use Case Documentation Policy]], [[AI Governance/Policies/AI Monitoring Policy]]
- ## Wikipedia Context
	- [Autonomous agent](https://en.wikipedia.org/wiki/Autonomous_agent): "an artificial intelligence (AI) system that can perform complex tasks independently."
	- [Intelligent agent](https://en.wikipedia.org/wiki/Intelligent_agent): "an entity that perceives its environment, takes actions autonomously to achieve goals, and may improve its performance through machine learning or by acquiring knowledge."
	- [Existential risk from AI](https://en.wikipedia.org/wiki/Existential_risk_from_artificial_intelligence): "substantial progress in artificial general intelligence (AGI) and artificial superintelligence (ASI) could lead to human extinction or an irreversible global catastrophe."
- ## See Also
	- [[Human-AI Relationships Glossary]]
	- [[AI as a Manager (AI-Led Decision Making)]]
	- [[AI Risks]]
	- [[AI Risks/Existential Risk]]
	- [[AI alignment]]
	- [[KnowYourAI]]
