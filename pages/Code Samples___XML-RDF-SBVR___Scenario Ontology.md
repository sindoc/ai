title:: Code Samples/XML-RDF-SBVR/Scenario Ontology
asset-code:: CSMP-RDF01
public:: true

- RDF/SKOS and SBVR-style vocabulary definitions for the AI Scenario ontology. These are the machine-readable counterparts to the Logseq graph pages, enabling Collibra import and [[SilkPage]] processing.
- ## RDF/SKOS — Scenario Concept Scheme
	- ```xml
	  <?xml version="1.0" encoding="UTF-8"?>
	  <rdf:RDF
	    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
	    xmlns:dcterms="http://purl.org/dc/terms/"
	    xmlns:ai="urn:ai-knowledge-graph:v1:">
	  
	    <skos:ConceptScheme rdf:about="urn:ai-knowledge-graph:scheme:scenario">
	      <dcterms:title>AI Life Scenario Ontology</dcterms:title>
	      <skos:prefLabel xml:lang="en">AI Life Scenario Ontology</skos:prefLabel>
	    </skos:ConceptScheme>
	  
	    <!-- ── Human-AI Role Concepts ────────────────────────────────── -->
	    <skos:Concept rdf:about="urn:ai-knowledge-graph:concept:AIRole">
	      <skos:prefLabel xml:lang="en">AI Role</skos:prefLabel>
	      <skos:topConceptOf rdf:resource="urn:ai-knowledge-graph:scheme:scenario"/>
	    </skos:Concept>
	  
	    <skos:Concept rdf:about="urn:ai-knowledge-graph:role:Tool">
	      <skos:prefLabel xml:lang="en">AI as a Tool (Human-Controlled AI)</skos:prefLabel>
	      <skos:notation>HAIR-T</skos:notation>
	      <skos:broader rdf:resource="urn:ai-knowledge-graph:concept:AIRole"/>
	      <ai:riskTier>Low</ai:riskTier>
	    </skos:Concept>
	  
	    <skos:Concept rdf:about="urn:ai-knowledge-graph:role:Assistant">
	      <skos:prefLabel xml:lang="en">AI as an Assistant (Collaborative AI)</skos:prefLabel>
	      <skos:notation>HAIR-A</skos:notation>
	      <skos:broader rdf:resource="urn:ai-knowledge-graph:concept:AIRole"/>
	      <ai:riskTier>Medium</ai:riskTier>
	    </skos:Concept>
	  
	    <skos:Concept rdf:about="urn:ai-knowledge-graph:role:Augmenter">
	      <skos:prefLabel xml:lang="en">AI as an Augmenter (Human-AI Symbiosis)</skos:prefLabel>
	      <skos:notation>HAIR-G</skos:notation>
	      <skos:broader rdf:resource="urn:ai-knowledge-graph:concept:AIRole"/>
	      <ai:riskTier>Medium</ai:riskTier>
	    </skos:Concept>
	  
	    <skos:Concept rdf:about="urn:ai-knowledge-graph:role:Manager">
	      <skos:prefLabel xml:lang="en">AI as a Manager (AI-Led Decision Making)</skos:prefLabel>
	      <skos:notation>HAIR-M</skos:notation>
	      <skos:broader rdf:resource="urn:ai-knowledge-graph:concept:AIRole"/>
	      <ai:riskTier>High</ai:riskTier>
	    </skos:Concept>
	  
	    <skos:Concept rdf:about="urn:ai-knowledge-graph:role:AutonomousAgent">
	      <skos:prefLabel xml:lang="en">AI as an Autonomous Agent (AI Independence)</skos:prefLabel>
	      <skos:notation>HAIR-AU</skos:notation>
	      <skos:broader rdf:resource="urn:ai-knowledge-graph:concept:AIRole"/>
	      <ai:riskTier>High</ai:riskTier>
	    </skos:Concept>
	  
	    <!-- ── Scenario Instance Example ─────────────────────────────── -->
	    <rdf:Description rdf:about="urn:ai-knowledge-graph:scenario:SCEN-001">
	      <rdf:type rdf:resource="urn:ai-knowledge-graph:concept:Scenario"/>
	      <dcterms:identifier>SCEN-001</dcterms:identifier>
	      <dcterms:title>Two LLMs Debate a Policy</dcterms:title>
	      <ai:namespace>Scenario/Multi-AI</ai:namespace>
	      <ai:participantRole rdf:resource="urn:ai-knowledge-graph:role:Assistant"/>
	    </rdf:Description>
	  
	  </rdf:RDF>
	  ```
- ## SBVR-Style Business Rules (plain language + structured)
	- The following rules are expressed in SBVR vocabulary style (plain-language first, formal constraint second):
	- ```
	  Vocabulary: AI Life Scenario Ontology
	  
	  Concept: Scenario
	    Definition: A documented event or interaction from AI's life involving at
	                least one AI system and at least one other participant.
	    Synonyms: AI scenario, AI life event
	  
	  Concept: Participant
	    Definition: An AI system or human involved in a Scenario.
	  
	  Concept: AI Role
	    Definition: One of five defined relationship modes between an AI system
	                and its principal (human or other AI).
	    Code Set: HAIR-T | HAIR-A | HAIR-G | HAIR-M | HAIR-AU
	  
	  Business Rule BR-001:
	    Statement: It is obligatory that each Scenario has at least two Participants.
	    Code: BRUL-001
	    Source: Scenario.md minimum requirements
	  
	  Business Rule BR-002:
	    Statement: It is obligatory that each Participant has exactly one AI Role.
	    Code: BRUL-002
	  
	  Business Rule BR-003:
	    Statement: It is obligatory that each Scenario has an asset-code
	                matching the pattern SCEN-[0-9]{3}.
	    Code: BRUL-003
	  
	  Business Rule BR-004:
	    Statement: It is prohibited for a Scenario with a High-risk AI Role to
	                be merged without a governance review annotation.
	    Code: BRUL-004
	    Applies to: AI as a Manager, AI as an Autonomous Agent
	  ```
- ## See Also
	- [[Collibra Operating Model]]
	- [[Code Samples/Python/Scenario Validator]]
	- [[Code Samples/Go/Pipeline Orchestrator]]
	- [[SilkPage]]
