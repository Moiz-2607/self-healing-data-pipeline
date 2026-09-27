# Self-Healing Data Engineering Pipeline Agent

A risk-aware data engineering pipeline that detects schema drift, diagnoses failures, performs safe automatic repairs, validates repaired data, rolls back unsafe changes, records an audit trail, and generates alerts when human intervention is required.

## Overview

Data pipelines can fail when incoming datasets change unexpectedly.

Examples include:

- A required column disappears.
- A column is renamed.
- A datatype changes unexpectedly.
- An automatic repair produces invalid data.

This project implements a cautious self-healing approach.

The system combines deterministic data-quality rules with AI-assisted diagnosis and a risk-aware decision engine.

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
Deterministic          AI Diagnosis
Diagnosis                   |
      |                     |
      +----------+----------+
                 |
                 v
        Recovery Decision
                 |
       +---------+---------+
       |                   |
       v                   v
   AUTO_REPAIR        HUMAN_REVIEW
       |                   |
       v                   v
    Repair              Alert
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
