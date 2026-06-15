title:: AI as an Assistant (Collaborative AI)
alias:: Collaborative AI, AI Assistant
asset-code:: HAIR-A
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Virtual_assistant
risk-tier:: Medium

- **AI as an Assistant** is the role in the [[Human-AI Relationships Glossary]] where an AI system actively participates in a task alongside a human, offering suggestions, drafts, or analysis — while the human retains final decision authority.
- ## Definition
	- The assistant role is distinguished from the tool role by **dialogue and initiative**: an assistant can proactively surface relevant information, ask clarifying questions, and propose next steps. The human remains the principal; the AI is a collaborative partner, not a co-equal decision-maker.
	- Wikipedia defines a virtual assistant as "a software agent that can perform a range of tasks or services for a user based on user input, such as commands or questions… The interaction may be via text, graphical interface, or voice." In the Collaborative AI role, the interaction is iterative and conversational rather than single-shot.
	- Most contemporary [[Large Language Model]]-based products (Claude, GPT-4, Gemini) operate in this role by default: they respond to prompts, maintain conversational context, and offer multi-turn refinement.
- ## Characteristics
	- **Proactive contribution** — the AI surfaces context, alternatives, and risks the human may not have asked for
	- **Stateful dialogue** — conversation history informs subsequent responses
	- **Human override always available** — the AI's output is advisory; the human can reject or modify it
	- **Partial autonomy** — the AI can choose *how* to answer, but not *whether* to act on the world
	- **Bidirectional feedback** — the human can correct, redirect, or extend the AI's outputs
- ## Risk Profile
	- **Risk tier**: Medium
	- Key risks in the assistant role:
		- **Over-reliance** — human may defer to AI output without sufficient verification ([[AI Risks/Automation Bias]])
		- **Hallucination** — AI may present plausible but false information confidently
		- **Consent and privacy** — conversations may inadvertently expose sensitive data
		- **Accountability gap** — unclear whether human or AI "owns" an output
		- **Political or ideological bias** — LLMs trained on web-scale data encode cultural perspectives
	- High-frequency assistant deployments (customer service, medical triage) require additional governance controls. See [[AI Governance/Policies/AI Use Case Documentation Policy]].
- ## Examples in Practice
	- A coding assistant (Copilot, Claude Code) suggesting code completions
	- An LLM drafting a governance policy for human review
	- A legal research assistant surfacing relevant case law
	- A medical information assistant presenting differential diagnoses
	- Two LLM assistants arguing opposing sides of a policy (see [[Scenario/Multi-AI/001/Two LLMs Debate a Policy]])
- ## Governance Markers
	- `asset-code:: HAIR-A`
	- Required disclosure: users must be informed they are interacting with an AI
	- Applicable policy: [[AI Governance/Policies/AI Use Case Documentation Policy]], [[AI Governance/Policies/AI Monitoring Policy]]
	- Audit trail: interaction logs should be retained for high-stakes decisions
- ## Wikipedia Context
	- [Virtual assistant](https://en.wikipedia.org/wiki/Virtual_assistant): "a software agent that can perform a range of tasks or services for a user based on user input, such as commands or questions… The interaction may be via text, graphical interface, or voice."
	- [Intelligent agent](https://en.wikipedia.org/wiki/Intelligent_agent): "an entity that perceives its environment, takes actions autonomously to achieve goals, and may improve its performance through machine learning."
- ## Code Sample
	- [[Code Samples/Python/Scenario Validator]] — orchestrating multi-turn assistant calls in a governed pipeline
- ## See Also
	- [[Human-AI Relationships Glossary]]
	- [[AI as a Tool (Human-Controlled AI)]]
	- [[AI as an Augmenter (Human-AI Symbiosis)]]
	- [[AI Risks]]
	- [[Large Language Model]]
	- [[KnowYourAI]]
