title:: Code Samples/Go/Pipeline Orchestrator
asset-code:: CSMP-GO01
public:: true

- A Go implementation of the scenario-lifecycle event orchestrator: receives submission events, validates against the [[Orchestration/Data Contract]], routes to enrichment services, and emits audit records to the observability layer.
- ## Source
	- Language: Go 1.22+
	- Dependencies: `encoding/json`, `net/http`, `log/slog` (stdlib only)
- ## Code
	- ```go
	  // pipeline_orchestrator.go
	  // Scenario lifecycle event orchestrator. Receives POST /submit,
	  // validates the data contract, fans out to enrichment, emits structured logs.
	  package main
	  
	  import (
	  	"encoding/json"
	  	"log/slog"
	  	"net/http"
	  	"os"
	  	"time"
	  )
	  
	  type Participant struct {
	  	Name     string `json:"name"`
	  	Provider string `json:"model_provider"`
	  	Role     string `json:"role"`
	  }
	  
	  type ScenarioSubmission struct {
	  	AssetCode    string        `json:"asset_code"`
	  	Namespace    string        `json:"namespace"`
	  	Participants []Participant `json:"participants"`
	  	Description  string        `json:"description"`
	  	DateProposed string        `json:"date_proposed"`
	  }
	  
	  type AuditEvent struct {
	  	Timestamp   time.Time          `json:"timestamp"`
	  	EventType   string             `json:"event_type"`
	  	AssetCode   string             `json:"asset_code"`
	  	Namespace   string             `json:"namespace"`
	  	Valid        bool               `json:"valid"`
	  	Errors      []string           `json:"errors,omitempty"`
	  	DurationMs  int64              `json:"duration_ms"`
	  }
	  
	  var logger = slog.New(slog.NewJSONHandler(os.Stdout, nil))
	  
	  func validate(s ScenarioSubmission) []string {
	  	var errs []string
	  	if s.AssetCode == "" {
	  		errs = append(errs, "asset_code is required")
	  	}
	  	if len(s.Participants) < 2 {
	  		errs = append(errs, "at least two participants required")
	  	}
	  	for i, p := range s.Participants {
	  		if p.Role == "" {
	  			errs = append(errs, fmt.Sprintf("participant[%d].role is required", i))
	  		}
	  	}
	  	return errs
	  }
	  
	  func submitHandler(w http.ResponseWriter, r *http.Request) {
	  	start := time.Now()
	  	var submission ScenarioSubmission
	  	if err := json.NewDecoder(r.Body).Decode(&submission); err != nil {
	  		http.Error(w, "invalid JSON", http.StatusBadRequest)
	  		return
	  	}
	  
	  	errs := validate(submission)
	  	audit := AuditEvent{
	  		Timestamp: time.Now().UTC(),
	  		EventType: "scenario.submitted",
	  		AssetCode: submission.AssetCode,
	  		Namespace: submission.Namespace,
	  		Valid:      len(errs) == 0,
	  		Errors:    errs,
	  		DurationMs: time.Since(start).Milliseconds(),
	  	}
	  	logger.Info("scenario_submission", "audit", audit)
	  
	  	status := http.StatusAccepted
	  	if !audit.Valid {
	  		status = http.StatusUnprocessableEntity
	  	}
	  	w.Header().Set("Content-Type", "application/json")
	  	w.WriteHeader(status)
	  	json.NewEncoder(w).Encode(audit)
	  }
	  
	  func main() {
	  	mux := http.NewServeMux()
	  	mux.HandleFunc("POST /submit", submitHandler)
	  	mux.HandleFunc("GET /health", func(w http.ResponseWriter, _ *http.Request) {
	  		w.WriteHeader(http.StatusOK)
	  	})
	  	logger.Info("starting pipeline orchestrator", "addr", ":8080")
	  	http.ListenAndServe(":8080", mux)
	  }
	  ```
- ## Notes
	- This Go service acts as the entry point for the [[Orchestration/Scenario Lifecycle BPMN]] pipeline
	- Structured JSON logs are ingested by the [[Orchestration/Observability]] layer
	- For production, add mTLS, rate limiting, and PostgreSQL persistence (see `schema/postgresql-init.sql`)
- ## See Also
	- [[Code Samples/Python/Scenario Validator]]
	- [[Code Samples/Rust/Subscriber Import Adapter]]
	- [[Code Samples/XML-RDF-SBVR/Scenario Ontology]]
	- [[Singine]]
	- [[SilkPage]]
