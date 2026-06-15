title:: AI as an Augmenter (Human-AI Symbiosis)
alias:: Human-AI Symbiosis, Augmenter AI, Augmented Intelligence
asset-code:: HAIR-G
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Augmented_intelligence
risk-tier:: Medium

- **AI as an Augmenter** is the role in the [[Human-AI Relationships Glossary]] where an AI system and a human operate as a tightly-coupled unit, each amplifying the other's capabilities to a degree that neither could achieve independently.
- ## Definition
	- In the augmenter role, the boundary between human cognition and AI assistance becomes permeable. The AI does not merely respond — it continuously adapts to the human's workflow, provides real-time feedback, and over time shapes how the human thinks about the problem domain.
	- Wikipedia describes this as **intelligence amplification (IA)**: "the use of information technology to enhance human cognitive capabilities, such as reasoning, learning, problem-solving, and decision-making, **rather than replacing human intelligence** with autonomous artificial systems."
	- The augmenter role differs from the assistant role in degree and coupling: in augmentation, the AI's outputs are integrated into the human's perceptual loop (dashboards, annotations, decision-support overlays), not merely consulted on request.
- ## Characteristics
	- **Tight coupling** — AI output is embedded in the human's workspace, not delivered as discrete responses
	- **Adaptive personalisation** — the AI learns the human's preferences and working patterns over time
	- **Shared cognitive load** — attention, memory, and pattern-recognition are distributed across human and AI
	- **Emergent capability** — the human-AI pair achieves outcomes neither could reach alone
	- **Latent autonomy risk** — the more tightly coupled, the harder it is to disentangle human from AI judgement
- ## Risk Profile
	- **Risk tier**: Medium (escalating toward High in safety-critical contexts)
	- Key risks in the augmenter role:
		- **[[Human Value Drift]]** — sustained exposure to AI-shaped outputs can gradually shift the human's values and judgements without conscious awareness
		- **Skill atrophy** — humans may lose proficiency in skills the AI now handles
		- **Accountability diffusion** — when a decision emerges from a tight human-AI loop, attributing responsibility is legally and ethically complex
		- **Lock-in** — the human becomes dependent on a specific AI system's biases and blind spots
	- Symbiosis contexts (clinical decision support, cockpit automation, financial modelling) warrant explicit drift monitoring. See [[AI Governance/Policies/AI Monitoring Policy]].
- ## Examples in Practice
	- A radiologist using AI-overlay diagnostics (the AI marks regions; the radiologist's eye is trained to the AI's visual vocabulary)
	- A composer using an AI accompaniment system that learns and extends the composer's musical style
	- A developer pair-programming with an AI that has learned the codebase's idioms
	- An analyst using an AI that prefilters and scores incoming signals before the analyst sees them
- ## Governance Markers
	- `asset-code:: HAIR-G`
	- Required disclosure: users interacting with AI-augmented professionals must be informed where applicable (clinical, legal contexts)
	- Drift monitoring: periodic human-only performance baselines to detect skill atrophy
	- Applicable policy: [[AI Governance/Policies/AI Monitoring Policy]]
- ## Wikipedia Context
	- [Augmented intelligence](https://en.wikipedia.org/wiki/Augmented_intelligence): "the use of information technology to enhance human cognitive capabilities… rather than replacing human intelligence with autonomous artificial systems. The idea was first proposed in the 1950s and 1960s by cybernetics and early computer pioneers."
- ## See Also
	- [[Human-AI Relationships Glossary]]
	- [[AI as an Assistant (Collaborative AI)]]
	- [[AI as a Manager (AI-Led Decision Making)]]
	- [[Human Value Drift]]
	- [[AI Risks]]
	- [[KnowYourAI]]
