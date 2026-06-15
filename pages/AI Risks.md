title:: AI Risks
alias:: AI Risk, Risks of AI
asset-code:: AIRK
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/AI_safety

- **AI Risks** is a structured taxonomy of harms, failure modes, and systemic dangers arising from AI systems across the five roles defined in the [[Human-AI Relationships Glossary]].
- Wikipedia on [[AI safety]]: "an interdisciplinary field focused on preventing accidents, misuse, or other harmful consequences arising from artificial intelligence systems."
- ## Risk Tiers
	- | Role | Risk Tier | Primary Risk Class |
	  |------|-----------|-------------------|
	  | [[AI as a Tool (Human-Controlled AI)]] | Low | Input quality; human misuse |
	  | [[AI as an Assistant (Collaborative AI)]] | Medium | Over-reliance; hallucination; privacy |
	  | [[AI as an Augmenter (Human-AI Symbiosis)]] | Medium–High | Value drift; accountability diffusion |
	  | [[AI as a Manager (AI-Led Decision Making)]] | High | Disparate impact; accountability vacuum |
	  | [[AI as an Autonomous Agent (AI Independence)]] | High–Critical | Goal misspecification; resource acquisition; existential |
- ## Risk Categories
- ### Technical Risks
	- **Hallucination** — confident generation of factually incorrect content by [[Large Language Model]]s
		- Wikipedia: see [Hallucination (artificial intelligence)](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence))
	- **[[Concept Drift]]** — statistical shift in data distributions that degrades model performance after deployment
		- Wikipedia: "an evolution of data that invalidates the data model… causes problems because the predictions become less accurate as time passes."
	- **Adversarial inputs** — inputs crafted to cause misclassification or harmful outputs
	- **Model collapse** — performance degradation when models are trained on AI-generated data rather than human-generated data
- ### Societal Risks
	- **Bias and discrimination** — systematic unfairness toward groups defined by protected characteristics; see [[AI Governance/Sensitive Attributes]]
	- **Misinformation at scale** — AI-generated content that is false, misleading, or designed to manipulate public opinion
	- **Surveillance and privacy** — AI systems enabling mass surveillance or privacy erosion
	- **Labour displacement** — automation of cognitive tasks at scale without adequate transition planning
	- **[[Human Value Drift]]** — gradual shift in human values due to sustained AI-mediated environments
- ### Governance Risks
	- **Accountability vacuum** — when AI makes decisions, it is unclear which human or organisation bears legal and moral responsibility
	- **Regulatory arbitrage** — deploying AI in jurisdictions with weaker governance to circumvent stricter rules
	- **Audit opacity** — inability to inspect AI decision logic (see [[blackbox testing]])
	- **Concentration of power** — AI capabilities concentrated in a small number of commercial actors (see [[Anthropic]], [[OpenAI]], [[Google]], [[Meta]], [[Mistral AI]])
- ### Existential Risks
	- **[[AI Risks/Existential Risk]]** — risks that AI development leads to outcomes catastrophic at civilisational scale
		- Wikipedia on existential risk from AI: "substantial progress in artificial general intelligence (AGI) and artificial superintelligence (ASI) could lead to human extinction or an irreversible global catastrophe."
	- **Misalignment** — an AI pursuing an objective misspecified relative to human values
		- Wikipedia on [[AI alignment]]: "alignment aims to steer AI systems toward a person's or group's intended goals, preferences, or ethical principles. A misaligned AI system pursues unintended objectives."
- ## Mitigation Approaches
	- **[[AI Governance]]** — policy and process frameworks (EU AI Act, NIST AI RMF, ISO 42001)
	- **Red-teaming and [[blackbox testing]]** — adversarial evaluation before and during deployment
	- **Drift monitoring** — continuous tracking of output distributions (see [[AI Governance/Tools/NannyML]])
	- **Human-in-the-loop gates** — mandatory human review for high-stakes decisions
	- **[[AI alignment]] research** — technical work on specifying and enforcing value alignment in AI systems
	- **Data contracts** — formalised agreements on data quality and schema (see [[Orchestration/Data Contract]])
- ## Scenario Coverage
	- | Scenario | Risk(s) Illustrated |
	  |----------|-------------------|
	  | [[Scenario/Multi-AI/001/Two LLMs Debate a Policy]] | Political bias; divergence between models |
	  | [[Scenario/Human-AI/002/AI Content Moderation Escalation]] | Accountability vacuum; disparate impact |
	  | [[Scenario/Human-AI/003/AI Diagnostic vs Human Override]] | Over-reliance; automation bias |
	  | [[Scenario/Multi-AI/004/Multi-LLM Code Review Pipeline]] | Hallucination in technical context |
	  | [[Scenario/Multi-AI/005/Autonomous Trading Agent with Oversight AI]] | Goal misspecification; resource acquisition |
- ## See Also
	- [[Human-AI Relationships Glossary]]
	- [[AI Governance]]
	- [[KnowYourAI]]
	- [[AI alignment]]
