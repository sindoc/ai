#!/usr/bin/env python3
"""
observability.py — structured logging and drift-detection hooks for the
AI Life scenario lifecycle pipeline.

Emits JSON-structured events to stdout (ingested by any log aggregator).
Provides hooks for:
  - scenario submission events
  - validation pass/fail
  - Wikipedia enrichment calls
  - Collibra registration
  - publication events
  - drift detection against the baseline health check
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class EventType(str, Enum):
    SCENARIO_SUBMITTED      = "scenario.submitted"
    VALIDATION_PASSED       = "validation.passed"
    VALIDATION_FAILED       = "validation.failed"
    ENRICHMENT_CALLED       = "enrichment.wikipedia.called"
    ENRICHMENT_HIT          = "enrichment.wikipedia.hit"
    ENRICHMENT_MISS         = "enrichment.wikipedia.miss"
    HEALTH_CHECK_PASSED     = "health_check.passed"
    HEALTH_CHECK_WARNED     = "health_check.warned"
    HEALTH_CHECK_FAILED     = "health_check.errored"
    COLLIBRA_REGISTERED     = "collibra.asset.registered"
    COLLIBRA_FAILED         = "collibra.asset.failed"
    PUBLICATION_STARTED     = "publication.started"
    PUBLICATION_DONE        = "publication.done"
    DRIFT_DETECTED          = "drift.detected"
    PIPELINE_ERROR          = "pipeline.error"


@dataclass
class ObservabilityEvent:
    event_type:   str
    asset_code:   str
    timestamp:    str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    duration_ms:  int | None = None
    namespace:    str | None = None
    risk_tier:    str | None = None
    details:      dict[str, Any] = field(default_factory=dict)
    errors:       list[str] = field(default_factory=list)
    warnings:     list[str] = field(default_factory=list)


class PipelineLogger:
    """Thin wrapper around structured JSON logging for the scenario pipeline."""

    def __init__(self, output=sys.stdout):
        self._out = output

    def emit(self, event: ObservabilityEvent) -> None:
        print(json.dumps(asdict(event), ensure_ascii=False), file=self._out, flush=True)

    def scenario_submitted(self, asset_code: str, namespace: str, risk_tier: str) -> None:
        self.emit(ObservabilityEvent(
            event_type=EventType.SCENARIO_SUBMITTED,
            asset_code=asset_code,
            namespace=namespace,
            risk_tier=risk_tier,
        ))

    def validation_result(self, asset_code: str, errors: list[str], duration_ms: int) -> None:
        evt = EventType.VALIDATION_PASSED if not errors else EventType.VALIDATION_FAILED
        self.emit(ObservabilityEvent(
            event_type=evt,
            asset_code=asset_code,
            duration_ms=duration_ms,
            errors=errors,
        ))

    def enrichment(self, asset_code: str, query: str, hit: bool, duration_ms: int) -> None:
        evt = EventType.ENRICHMENT_HIT if hit else EventType.ENRICHMENT_MISS
        self.emit(ObservabilityEvent(
            event_type=evt,
            asset_code=asset_code,
            duration_ms=duration_ms,
            details={"query": query},
        ))

    def health_check_result(self, asset_code: str, errors: int, warnings: int) -> None:
        if errors > 0:
            evt = EventType.HEALTH_CHECK_FAILED
        elif warnings > 0:
            evt = EventType.HEALTH_CHECK_WARNED
        else:
            evt = EventType.HEALTH_CHECK_PASSED
        self.emit(ObservabilityEvent(
            event_type=evt,
            asset_code=asset_code,
            details={"error_count": errors, "warning_count": warnings},
        ))

    def collibra_registration(self, asset_code: str, collibra_id: str | None, error: str | None = None) -> None:
        evt = EventType.COLLIBRA_REGISTERED if collibra_id else EventType.COLLIBRA_FAILED
        self.emit(ObservabilityEvent(
            event_type=evt,
            asset_code=asset_code,
            details={"collibra_asset_id": collibra_id},
            errors=[error] if error else [],
        ))

    def publication(self, asset_code: str, done: bool, duration_ms: int) -> None:
        evt = EventType.PUBLICATION_DONE if done else EventType.PUBLICATION_STARTED
        self.emit(ObservabilityEvent(
            event_type=evt,
            asset_code=asset_code,
            duration_ms=duration_ms,
        ))

    def drift_detected(self, asset_code: str, baseline_warnings: int, current_warnings: int) -> None:
        delta = current_warnings - baseline_warnings
        self.emit(ObservabilityEvent(
            event_type=EventType.DRIFT_DETECTED,
            asset_code=asset_code,
            details={
                "baseline_warnings": baseline_warnings,
                "current_warnings": current_warnings,
                "delta": delta,
            },
            warnings=[f"Health check warning count increased by {delta} since baseline"],
        ))


def run_health_check_and_detect_drift(baseline_path: Path | None = None) -> tuple[int, int]:
    """
    Run health_check.py and compare against a baseline snapshot.
    Returns (error_count, warning_count).
    Emits a drift event if warning count exceeds the stored baseline.
    """
    import subprocess
    repo_root = Path(__file__).parent.parent
    result = subprocess.run(
        [sys.executable, str(repo_root / "tools/health_check.py")],
        capture_output=True, text=True
    )
    output = result.stdout + result.stderr
    errors = output.count("[ERROR]")
    warnings = output.count("[WARN]")

    logger = PipelineLogger()

    if baseline_path and baseline_path.exists():
        baseline = json.loads(baseline_path.read_text())
        baseline_warnings = baseline.get("warnings", 0)
        if warnings > baseline_warnings:
            logger.drift_detected(
                asset_code="GRAPH",
                baseline_warnings=baseline_warnings,
                current_warnings=warnings,
            )

    if baseline_path:
        baseline_path.write_text(json.dumps({"warnings": warnings, "errors": errors,
                                              "timestamp": datetime.now(timezone.utc).isoformat()}))

    return errors, warnings


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run observability health check with drift detection")
    parser.add_argument("--baseline", type=Path, default=Path("orchestration/.health-baseline.json"),
                        help="Path to baseline snapshot JSON")
    args = parser.parse_args()

    errors, warnings = run_health_check_and_detect_drift(args.baseline)
    print(f"Health check: {errors} error(s), {warnings} warning(s)", file=sys.stderr)
    sys.exit(1 if errors else 0)
