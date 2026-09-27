# Self-Healing Data Engineering Pipeline Agent

A risk-aware data engineering pipeline that detects schema drift, diagnoses failures, performs safe recovery when appropriate, validates the repaired data, and rolls back failed repairs.

The system is designed around one principle:

> **Automation should be cautious, explainable, and reversible.**

AI is used as a supporting component for diagnosis and repair planning, while deterministic rules, risk classification, validation, and rollback remain responsible for keeping the pipeline safe.

---

## Overview

Data pipelines can fail when incoming data changes unexpectedly.

Examples include:

- Required columns disappearing
- Columns being renamed
- Datatypes changing
- Invalid values appearing in structured fields

Instead of simply failing or blindly modifying the data, this project evaluates the failure and chooses an appropriate recovery strategy.

Depending on the risk and confidence:

- Low-risk failures can be automatically repaired
- Medium-risk failures can receive AI-assisted suggestions
- High-risk failures require human review
- Every attempted repair is validated
- Failed repairs are rolled back
- Important events are recorded in an audit log
- Critical incidents can generate Slack alerts

---

## Core Flow

```text
Incoming Data
      |
      v
Schema Analysis
      |
      v
Schema Drift Detection
      |
      v
Risk Classification
      |
      +----------------------+
      |                      |
      v                      v
Deterministic           AI Diagnosis
Diagnosis                    |
      |                      |
      +----------+-----------+
                 |
                 v
        Recovery Decision
                 |
       +---------+---------+
       |                   |
       v                   v
  AUTO_REPAIR         HUMAN_REVIEW
       |                   |
       v                   v
    Repair               Alert
       |
       v
Post-Repair Validation
       |
    +--+--+
    |     |
    v     v
  PASS   FAIL
    |     |
    v     v
REPAIRED ROLLBACK
          |
          v
        Alert
