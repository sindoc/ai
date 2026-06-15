title:: knowledge graph
alias:: Knowledge Graph, knowledge graphs
asset-code:: KNWG
public:: true
wikipedia-url:: https://en.wikipedia.org/wiki/Knowledge_graph

- A **knowledge graph** is a structured representation of knowledge in which entities (people, places, concepts, events) are represented as nodes, and the relationships between them as labelled edges.
- Wikipedia: "a knowledge base that uses a graph-structured data model or topology to represent and operate on data. Knowledge graphs are often used to store interlinked descriptions of entities — objects, events, situations or abstract concepts — while also encoding the free-form semantics or relationships underlying these entities."
- ## This Repository as a Knowledge Graph
	- The `ai/` repository is a **Logseq knowledge graph** — a community-editable graph of pages connected by `[[wiki-links]]`. Each page is a node; each `[[reference]]` is an edge.
	- Logseq renders the graph as a force-directed visualisation in its Graph View, allowing community members to navigate relationships between scenarios, AI roles, governance concepts, and platform terms.
- ## Key Concepts in KG Terminology
	- **Node** — a page (e.g. `[[AI as an Assistant (Collaborative AI)]]`)
	- **Edge** — a `[[reference]]` inside the body of a page
	- **Property** — a `key:: value` line in page metadata (e.g. `asset-code:: SCEN-001`)
	- **Namespace** — a `/`-separated hierarchy (e.g. `Scenario/Multi-AI/001/...`)
	- **Alias** — alternative labels for the same node (`alias:: LLM, LLMs` in `[[Large Language Model]]`)
- ## See Also
	- [[AI Life]]
	- [[Logseq]]
	- [[SilkPage]]
	- [[Collibra Operating Model]]
