title:: Scenario/Human-AI/002/AI Content Moderation Escalation
asset-code:: SCEN-002
public:: true

- **ID**: `SCEN-002`
  **Namespace**: `Scenario/Human-AI`
  **Date Proposed**: 2026-06-14
  **Status**: Seed example
- ### Participants
	- **AI System 1**: Content Moderation LLM (e.g. GPT-4 fine-tuned for policy classification)
		- Model provider: [[OpenAI]]
		- Role: [[AI as a Manager (AI-Led Decision Making)]]
	- **Human participant**: Trust & Safety reviewer
		- Role: Appeals reviewer (handles escalations from the AI queue)
- ### Description
	- A social platform uses an LLM-based content moderation system to classify and action posts at scale. The AI reviews 500,000 posts per day and removes, labels, or escalates each one without human review of individual cases. Human reviewers only see the ~0.5% the AI escalates or the ~2% that users appeal.
	- In this scenario, the AI's classifier, trained primarily on English-language data, systematically over-flags minority-language content (Arabic-script posts) as potentially violating. The pattern only becomes visible when a human reviewer notices the demographic skew in the appeals queue.
	- The scenario explores: who is accountable when an AI manager makes thousands of discriminatory decisions before any human notices?
- ### Interaction Log or Link
	- *(Representative — based on documented moderation disparities reported by human rights organisations.)*
	- The reviewer escalates to [[AI Governance]] team, triggering a [[AI Governance/Policies/AI Monitoring Policy]] review.
- ### Governance Considerations
	- **Risk profile inherited**: [[AI as a Manager (AI-Led Decision Making)]] → High risk
	- **Applicable policies**: [[AI Governance/Policies/AI Use Case Documentation Policy]], [[AI Governance/Policies/AI Monitoring Policy]]
	- **Bias or sensitivity flags**: Language and script bias; see [[AI Governance/Sensitive Attributes]]
	- **Accountability gap**: The AI took the actions; the platform set the policy. Neither a human reviewer nor the AI "decided" at the individual post level.
- ### Why This Belongs in AI's Life
	- This scenario captures what it means for an AI to *manage at scale* — not just assist but decide, and to do so in a way that encodes the biases of its training environment into consequential real-world outcomes for thousands of people before any human checks.
- ### Code References
	- [[Code Samples/Python/Scenario Validator]] — validation pipeline used in this scenario's audit
	- [[Code Samples/Go/Pipeline Orchestrator]] — the moderation queue processing architecture
- ### References
	- [[AI Risks]]
	- [[Human-AI Relationships Glossary]]
	- [[AI Governance/Sensitive Attributes]]
