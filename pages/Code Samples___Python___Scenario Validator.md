title:: Code Samples/Python/Scenario Validator
asset-code:: CSMP-PY01
public:: true

- A Python implementation of the [[Orchestration/Data Contract]] validator and multi-step scenario orchestration pipeline. Demonstrates the [[AI as an Assistant (Collaborative AI)]] pattern: AI-as-tool calls wrapped in human-controlled validation logic.
- ## Source
	- Language: Python 3.11+
	- Runtime: `/usr/bin/python3` (system Python on macOS)
	- Dependencies: `httpx`, `jsonschema`, `pydantic`
- ## Code
	- ```python
	  """
	  scenario_validator.py — validate a scenario submission against the data contract
	  and orchestrate multi-LLM enrichment calls.
	  """
	  from __future__ import annotations
	  import json
	  import httpx
	  import jsonschema
	  from pathlib import Path
	  from dataclasses import dataclass, field
	  
	  CONTRACT_PATH = Path(__file__).parent.parent / "orchestration/data-contract.json"
	  
	  
	  @dataclass
	  class ScenarioSubmission:
	      asset_code: str
	      namespace: str
	      participants: list[dict] = field(default_factory=list)
	      description: str = ""
	      governance: dict = field(default_factory=dict)
	  
	  
	  def load_contract() -> dict:
	      return json.loads(CONTRACT_PATH.read_text())
	  
	  
	  def validate(submission: dict) -> list[str]:
	      """Returns list of validation errors; empty list means valid."""
	      contract = load_contract()
	      validator = jsonschema.Draft7Validator(contract)
	      return [e.message for e in validator.iter_errors(submission)]
	  
	  
	  def enrich_with_wikipedia(title: str, api_base: str = "https://en.wikipedia.org/api/rest_v1") -> dict | None:
	      """Fetch Wikipedia summary for a concept title."""
	      encoded = title.replace(" ", "_")
	      url = f"{api_base}/page/summary/{encoded}"
	      try:
	          r = httpx.get(url, timeout=10, headers={"User-Agent": "ai-knowledge-graph/1.0"})
	          if r.status_code == 200:
	              return r.json()
	      except httpx.RequestError:
	          pass
	      return None
	  
	  
	  def run_llm_call(provider: str, prompt: str, model: str) -> str:
	      """
	      Stub for a governed LLM call. In production, swap for the
	      provider's SDK (anthropic, openai, google-generativeai).
	      Logs call metadata for audit trail.
	      """
	      import datetime
	      log_entry = {
	          "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
	          "provider": provider,
	          "model": model,
	          "prompt_tokens": len(prompt.split()),
	      }
	      print(f"[audit] {json.dumps(log_entry)}")
	      return f"[stub response from {provider}/{model}]"
	  
	  
	  def orchestrate_review(submission: dict) -> dict:
	      """
	      Full pipeline: validate → enrich → request LLM governance review.
	      Returns a result dict with validation errors, enrichment, and review.
	      """
	      errors = validate(submission)
	      if errors:
	          return {"status": "invalid", "errors": errors}
	  
	      enrichment = {}
	      for participant in submission.get("participants", []):
	          role = participant.get("role", "")
	          if role:
	              enrichment[role] = enrich_with_wikipedia(role)
	  
	      review = run_llm_call(
	          provider="anthropic",
	          model="claude-sonnet-4-6",
	          prompt=f"Review governance considerations for scenario: {json.dumps(submission, indent=2)}",
	      )
	  
	      return {
	          "status": "ok",
	          "submission": submission,
	          "enrichment": enrichment,
	          "governance_review": review,
	      }
	  
	  
	  if __name__ == "__main__":
	      import sys
	      path = sys.argv[1] if len(sys.argv) > 1 else "orchestration/example-submission.json"
	      submission = json.loads(Path(path).read_text())
	      result = orchestrate_review(submission)
	      print(json.dumps(result, indent=2, default=str))
	  ```
- ## Usage
	- `python3 pages/Code\ Samples/Python/scenario_validator.py orchestration/example-submission.json`
- ## See Also
	- [[Orchestration/Data Contract]]
	- [[Code Samples/Rust/Subscriber Import Adapter]]
	- [[Code Samples/Go/Pipeline Orchestrator]]
