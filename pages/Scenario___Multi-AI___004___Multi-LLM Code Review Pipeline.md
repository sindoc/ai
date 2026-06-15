title:: Scenario/Multi-AI/004/Multi-LLM Code Review Pipeline
asset-code:: SCEN-004
public:: true

- **ID**: `SCEN-004`
  **Namespace**: `Scenario/Multi-AI`
  **Date Proposed**: 2026-06-14
  **Status**: Seed example
- ### Participants
	- **AI System 1**: Claude (code generation + initial review)
		- Model provider: [[Anthropic]]
		- Role: [[AI as an Assistant (Collaborative AI)]]
	- **AI System 2**: GPT-4 (secondary reviewer / adversarial critic)
		- Model provider: [[OpenAI]]
		- Role: [[AI as an Assistant (Collaborative AI)]]
	- **AI System 3**: Static analysis LLM (security-focused, e.g. CodeQL-backed)
		- Model provider: [[Meta]] (CodeLlama variant)
		- Role: [[AI as a Tool (Human-Controlled AI)]]
	- **Human participant**: Senior engineer
		- Role: Final approver; resolves AI reviewer disagreements
- ### Description
	- A software team implements a multi-stage code review pipeline for a security-critical module. Claude generates an initial implementation. GPT-4 acts as an adversarial reviewer, finding logical errors, edge cases, and security issues. A CodeLlama-based static analysis tool independently scans for known vulnerability patterns. The human engineer only reviews the delta — the disagreements between the two LLM reviewers and the findings from the static tool.
	- In this scenario, GPT-4 and Claude both miss a subtle integer overflow vulnerability because the pattern is present in their training data as a correct pattern in a different context. The static tool catches it. The scenario raises: what is the governance model for AI-to-AI review chains, and how do we know when the human's residual review is sufficient?
- ### Interaction Log or Link
	- *(Inspired by documented multi-LLM code review experiments in the AI engineering community.)*
- ### Governance Considerations
	- **Risk profile inherited**: [[AI as an Assistant (Collaborative AI)]] → Medium (composite; the chain as a whole is more autonomous than any single participant)
	- **Applicable policies**: [[AI Governance/Policies/AI Use Case Documentation Policy]]
	- **Systemic risk**: Two assistants with correlated training data may have correlated blind spots — the diversity benefit of multi-AI review depends on genuine independence of training.
- ### Why This Belongs in AI's Life
	- This scenario explores the emergent properties of AI-to-AI collaboration: can two AI systems, reviewing each other's outputs, achieve better reliability than either alone — or do shared training distributions create shared blind spots that no amount of AI-to-AI review can surface?
- ### Code References
	- [[Code Samples/Python/Scenario Validator]] — orchestrating multi-LLM API calls
	- [[Code Samples/Rust/Subscriber Import Adapter]] — the security-critical module being reviewed
	- [[Code Samples/Go/Pipeline Orchestrator]] — pipeline coordination layer
- ### References
	- [[AI Risks]]
	- [[Human-AI Relationships Glossary]]
	- [[AI Governance]]
