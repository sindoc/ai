title:: Scenario/Human-AI/003/AI Diagnostic vs Human Override
asset-code:: SCEN-003
public:: true

- **ID**: `SCEN-003`
  **Namespace**: `Scenario/Human-AI`
  **Date Proposed**: 2026-06-14
  **Status**: Seed example
- ### Participants
	- **AI System 1**: Clinical decision-support LLM (e.g. Med-PaLM 2 or similar)
		- Model provider: [[Google]]
		- Role: [[AI as an Augmenter (Human-AI Symbiosis)]]
	- **Human participant 1**: Radiologist (primary clinician)
		- Role: Reviewing AI-generated diagnostic overlay
	- **Human participant 2**: Patient
		- Role: Subject of diagnostic decision
- ### Description
	- A radiologist uses an AI-assisted diagnostic system that overlays probability scores on medical images. The AI flags a lung nodule as 87% probability malignant and recommends biopsy. The radiologist, reviewing the same scan without the overlay, assesses it as likely benign (scar tissue consistent with a prior infection). Under standard protocol, the AI recommendation must be documented and the human decision to override must be recorded with justification.
	- Three months later, follow-up imaging confirms the nodule was benign. The scenario asks: was the override justified? Should the system be recalibrated? Who bears responsibility if the human override had been wrong?
- ### Interaction Log or Link
	- *(Composite based on documented cases in clinical AI literature.)*
	- Override documented in the hospital's AI decision log (see [[Orchestration/Data Contract]] for log schema).
- ### Governance Considerations
	- **Risk profile inherited**: [[AI as an Augmenter (Human-AI Symbiosis)]] → Medium-High risk
	- **Applicable policies**: [[AI Governance/Policies/AI Monitoring Policy]], [[AI Governance/Policies/AI Use Case Documentation Policy]]
	- **Bias or sensitivity flags**: Training data demographics; scanner model and population distribution mismatch
	- **Key tension**: The AI's role is augmentation — the human retains authority to override. But the very act of presenting an 87% probability changes how the radiologist perceives the image ([[Human Value Drift]] at the individual cognitive level).
- ### Why This Belongs in AI's Life
	- This scenario illustrates how an AI, even in a supportive augmenter role, shapes the epistemic environment for the human. The AI's stated confidence becomes part of the clinical context before the clinician has formed their own judgement — a subtle but consequential form of AI influence on human cognition.
- ### Code References
	- [[Code Samples/Python/Scenario Validator]]
	- [[Code Samples/XML-RDF-SBVR/Scenario Ontology]] — the override event modelled in SBVR
- ### References
	- [[AI Risks]]
	- [[Human Value Drift]]
	- [[Human-AI Relationships Glossary]]
