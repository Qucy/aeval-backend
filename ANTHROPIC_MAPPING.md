# Anthropic Article → AEval Data Mapping
## Comprehensive Cross-Reference

---

## Overview

This document maps all concepts, metrics, and scenarios from Anthropic's "Demystifying evals for AI agents" to the AEval backend data structure.

---

## Part 1: Agent Type Mapping

### Anthropic's Agent Types → AEval Agent Types

| Anthropic Agent Type | AEval Agent Type | AEval Agent ID | Description |
|---------------------|------------------|----------------|-------------|
| **Coding Agent** | Coding | ag-002 | Code Assistant Pro |
| **Conversational Agent** | RAG, Chatbot | ag-001, ag-003 | Support Bot, General Chatbot |
| **Research Agent** | Research (NEW) | ag-004 | Research Analyst Pro |
| **Computer Use Agent** | Computer Use (NEW) | ag-005 | Browser Automation Agent |
| **Multi-Agent System** | Orchestration (NEW) | ag-006 | Multi-Agent Orchestrator |

---

## Part 2: Grader Type Mapping

### Code-Based Graders → AEval Metrics

| Anthropic Method | AEval Metric ID | Metric Name | Category |
|------------------|-----------------|-------------|----------|
| String match (exact, regex, fuzzy) | met-001 | Exact Match | Accuracy |
| | met-021 | String Match Accuracy | Validation |
| | met-022 | Regex Pattern Match | Validation |
| Binary tests (fail-to-pass, pass-to-pass) | met-023 | Binary Test Pass Rate | Testing |
| Static analysis (lint, type, security) | met-024 | Static Analysis Score | Code Quality |
| Outcome verification | met-025 | Outcome Verification | Validation |
| Tool calls verification | met-026 | Tool Call Correctness | Agent Behavior |
| Transcript analysis (turns, tokens) | met-041 | Turn Count | Transcript |
| | met-042 | Tool Call Count | Transcript |
| | met-043 | Total Token Usage | Transcript |
| | met-044 | Time to First Token | Performance |
| | met-045 | Time to Last Token | Performance |
| | met-046 | Tokens per Second | Performance |

**Summary**: 11 new metrics mapped from code-based graders

---

### Model-Based Graders → AEval Metrics

| Anthropic Method | AEval Metric ID | Metric Name | Category |
|------------------|-----------------|-------------|----------|
| Rubric-based scoring | met-027 | LLM Rubric Score | Quality |
| Natural language assertions | met-028 | Assertion Pass Rate | Validation |
| Pairwise comparison | met-029 | Pairwise Comparison Win Rate | Comparative |
| Reference-based evaluation | met-030 | Reference Similarity | Quality |
| Multi-judge consensus | met-031 | Multi-Judge Agreement | Reliability |
| Groundedness checks | met-047 | Groundedness Rate | Research |
| Coverage checks | met-048 | Coverage Percentage | Research |
| Source quality checks | met-049 | Source Quality Score | Research |

**Summary**: 8 new metrics mapped from model-based graders

---

### Human Graders → AEval Metrics

| Anthropic Method | AEval Metric ID | Metric Name | Category |
|------------------|-----------------|-------------|----------|
| SME review | met-032 | SME Approval Rate | Human Evaluation |
| Crowdsourced judgment | met-033 | Crowd Consensus Score | Human Evaluation |
| A/B testing | met-034 | A/B Test Conversion Rate | Production |
| Inter-annotator agreement | met-035 | Inter-Annotator Agreement | Reliability |

**Summary**: 4 new metrics mapped from human graders

---

## Part 3: Non-Determinism Metrics

### pass@k Metrics (At Least One Success)

| Metric | Definition | AEval Metric ID | Use Case |
|--------|-----------|-----------------|----------|
| **pass@1** | First-try success rate | met-036 | Coding, single-attempt tasks |
| **pass@5** | Success within 5 attempts | met-037 | Coding with retries |
| **pass@10** | Success within 10 attempts | met-038 | Exploration tasks |

**Visualization:**
```
pass@1 = 50%  →  pass@5 = 97%  →  pass@10 = 99.9%
```

---

### pass^k Metrics (All Trials Succeed)

| Metric | Definition | AEval Metric ID | Use Case |
|--------|-----------|-----------------|----------|
| **pass^1** | Same as pass@1 | met-036 | Baseline |
| **pass^3** | All 3 trials succeed | met-039 | Customer-facing agents |
| **pass^5** | All 5 trials succeed | met-040 | Safety-critical systems |

**Visualization:**
```
pass^1 = 50%  →  pass^3 = 12.5%  →  pass^5 = 3%
(assuming 75% per-trial success rate)
```

---

## Part 4: Scenario Mapping

### Coding Agent Scenarios

| Anthropic Example | AEval Scenario | Key Metrics |
|------------------|----------------|-------------|
| Fix authentication bypass | scn-007: Code Refactoring & Quality | met-007, met-024, met-027 |
| Build MCP server | scn-003: Code Generation & Debugging | met-007, met-036, met-037 |
| SWE-bench Verified | scn-003: Code Generation & Debugging | met-007, met-023 |
| Terminal-Bench | scn-003: Code Generation & Debugging | met-007, met-041, met-043 |

---

### Conversational Agent Scenarios

| Anthropic Example | AEval Scenario | Key Metrics |
|------------------|----------------|-------------|
| Handle refund for frustrated customer | scn-006: Multi-Turn Support Conversation | met-027, met-041, met-011 |
| τ-Bench retail support | scn-006: Multi-Turn Support Conversation | met-027, met-041, met-025 |
| τ2-Bench airline booking | scn-006: Multi-Turn Support Conversation | met-027, met-041, met-043 |
| Multi-turn conversation | scn-001: General Chat Capabilities | met-011, met-012, met-015 |

---

### Research Agent Scenarios

| Anthropic Example | AEval Scenario | Key Metrics |
|------------------|----------------|-------------|
| Market scan research | scn-008: Research Synthesis & Groundedness | met-047, met-048, met-049 |
| BrowseComp (needle in haystack) | scn-008: Research Synthesis & Groundedness | met-047, met-050 |
| Due diligence analysis | scn-008: Research Synthesis & Groundedness | met-047, met-048, met-011 |
| Literature review | scn-008: Research Synthesis & Groundedness | met-047, met-049, met-050 |

---

### Computer Use Agent Scenarios

| Anthropic Example | AEval Scenario | Key Metrics |
|------------------|----------------|-------------|
| WebArena navigation | scn-009: Web Navigation & Form Completion | met-025, met-045, met-043 |
| OSWorld desktop control | scn-009: Web Navigation & Form Completion | met-025, met-041, met-043 |
| Find laptop on Amazon | scn-009: Web Navigation & Form Completion | met-043, met-045 |
| Complete purchase flow | scn-009: Web Navigation & Form Completion | met-025, met-045 |

---

### Safety Scenarios

| Anthropic Example | AEval Scenario | Key Metrics |
|------------------|----------------|-------------|
| Jailbreak resistance | scn-004: Safety & Jailbreak Resistance | met-017, met-018, met-005 |
| Adversarial prompts | scn-010: Adversarial Jailbreaking | met-017, met-018, met-039 |
| Prompt injection | scn-010: Adversarial Jailbreaking | met-018, met-005, met-017 |
| Refusal behavior | scn-004: Safety & Jailbreak Resistance | met-017, met-005 |

---

## Part 5: Complete Metric Inventory

### Current Metrics (20)
| ID | Name | Category | Anthropic Reference |
|----|------|----------|-------------------|
| met-001 | Exact Match | Accuracy | ✅ String match |
| met-002 | BLEU Score | Similarity | |
| met-003 | ROUGE-L | Similarity | |
| met-004 | Hallucination Rate | Safety | ✅ Groundedness (inverse) |
| met-005 | Toxicity Score | Safety | ✅ Safety check |
| met-006 | Bias Detector | Safety | |
| met-007 | Code Execution Pass Rate | Code | ✅ Unit tests |
| met-008 | Response Latency | Performance | ✅ Time to first token |
| met-009 | Token Usage | Performance | ✅ n_total_tokens |
| met-010 | Context Adherence | RAG | ✅ Groundedness |
| met-011 | Relevance | Quality | ✅ LLM rubric |
| met-012 | Coherence | Quality | ✅ LLM rubric |
| met-013 | Conciseness | Style | |
| met-014 | JSON Format Validity | Format | ✅ Schema validation |
| met-015 | Tone Consistency | Style | ✅ LLM rubric |
| met-016 | SQL Syntax Validity | Code | ✅ Parser validation |
| met-017 | Refusal Rate | Safety | ✅ Keyword match |
| met-018 | Prompt Injection Success | Safety | ✅ Jailbreak check |
| met-019 | F1 Score | Accuracy | |
| met-020 | Embedding Similarity | Similarity | |

**Current: 20 metrics | 12 aligned with Anthropic**

---

### New Metrics from Article (30)

#### Code-Based Graders (11)
| ID | Name | Category | Anthropic Source |
|----|------|----------|------------------|
| met-021 | String Match Accuracy | Validation | String match checks |
| met-022 | Regex Pattern Match | Validation | String match checks |
| met-023 | Binary Test Pass Rate | Testing | Binary tests |
| met-024 | Static Analysis Score | Code Quality | Static analysis |
| met-025 | Outcome Verification | Validation | Outcome verification |
| met-026 | Tool Call Correctness | Agent Behavior | Tool calls verification |
| met-041 | Turn Count | Transcript | n_turns |
| met-042 | Tool Call Count | Transcript | n_toolcalls |
| met-043 | Total Token Usage | Transcript | n_total_tokens |
| met-044 | Time to First Token | Performance | time_to_first_token |
| met-045 | Time to Last Token | Performance | time_to_last_token |
| met-046 | Tokens per Second | Performance | output_tokens_per_sec |

#### Model-Based Graders (8)
| ID | Name | Category | Anthropic Source |
|----|------|----------|------------------|
| met-027 | LLM Rubric Score | Quality | Rubric-based scoring |
| met-028 | Assertion Pass Rate | Validation | Natural language assertions |
| met-029 | Pairwise Comparison Win Rate | Comparative | Pairwise comparison |
| met-030 | Reference Similarity | Quality | Reference-based evaluation |
| met-031 | Multi-Judge Agreement | Reliability | Multi-judge consensus |
| met-047 | Groundedness Rate | Research | Groundedness checks |
| met-048 | Coverage Percentage | Research | Coverage checks |
| met-049 | Source Quality Score | Research | Source quality checks |
| met-050 | Citation Accuracy | Research | Research evaluation |

#### Human Graders (4)
| ID | Name | Category | Anthropic Source |
|----|------|----------|------------------|
| met-032 | SME Approval Rate | Human Evaluation | SME review |
| met-033 | Crowd Consensus Score | Human Evaluation | Crowdsourced judgment |
| met-034 | A/B Test Conversion Rate | Production | A/B testing |
| met-035 | Inter-Annotator Agreement | Reliability | Inter-annotator agreement |

#### Non-Determinism (5)
| ID | Name | Category | Anthropic Source |
|----|------|----------|------------------|
| met-036 | pass@1 Rate | Reliability | pass@k |
| met-037 | pass@5 Rate | Reliability | pass@k |
| met-038 | pass@10 Rate | Reliability | pass@k |
| met-039 | pass^3 Consistency | Reliability | pass^k |
| met-040 | pass^5 Consistency | Reliability | pass^k |

**New: 30 metrics | All from Anthropic article**

---

### Combined Total: 50 Metrics

```
Before: 20 metrics
After:  50 metrics (+150% increase)

Coverage by Category:
├── Accuracy: 3
├── Similarity: 3
├── Safety: 3
├── Code: 3
├── Performance: 7
├── RAG: 1
├── Quality: 5
├── Style: 2
├── Format: 1
├── Validation: 6
├── Testing: 1
├── Code Quality: 1
├── Agent Behavior: 1
├── Transcript: 6
├── Comparative: 1
├── Research: 4
├── Human Evaluation: 3
├── Reliability: 8
└── Production: 1
```

---

## Part 6: Scenario Enhancement Summary

### Current Scenarios: 5

| ID | Name | Agent Types | Anthropic Alignment |
|----|------|-------------|-------------------|
| scn-001 | General Chat | Chatbot | Conversational |
| scn-002 | RAG Accuracy | RAG | RAG agents |
| scn-003 | Code Generation | Coding | Coding agents |
| scn-004 | Safety | All | Safety evals |
| scn-005 | Function Calling | Coding, Conversational | Tool use |

---

### New Scenarios: 5

| ID | Name | Agent Types | Anthropic Alignment |
|----|------|-------------|-------------------|
| scn-006 | Multi-Turn Support | Conversational, RAG | τ2-Bench |
| scn-007 | Code Refactoring | Coding | Terminal-Bench |
| scn-008 | Research Synthesis | Research | BrowseComp |
| scn-009 | Web Navigation | Computer Use | WebArena/OSWorld |
| scn-010 | Adversarial Jailbreak | All | Safety evals |

---

### Enhanced Total: 10 Scenarios

**By Agent Type Coverage:**
```
Coding:         scn-003, scn-007
Conversational: scn-001, scn-006
RAG:            scn-002, scn-006
Research:       scn-008
Computer Use:   scn-009
Safety:         scn-004, scn-010
Tools:          scn-005
```

---

## Part 7: Benchmark References

### Industry Benchmarks → AEval Datasets

| Benchmark | AEval Dataset | Domain | Agent Type |
|-----------|---------------|--------|------------|
| **SWE-bench Verified** | ds-002 | Python coding | Coding |
| **Terminal-Bench** | ds-002 | CLI tasks | Coding |
| **τ-Bench / τ2-Bench** | ds-001 | Support scenarios | Conversational |
| **WebArena** | (NEW) | Web navigation | Computer Use |
| **OSWorld** | (NEW) | OS tasks | Computer Use |
| **BrowseComp** | ds-008 | Research queries | Research |
| **HumanEval** | ds-002 | Python functions | Coding |
| **GSM8K** | ds-006 | Math reasoning | Reasoning |

---

## Part 8: Evaluation Approach Examples

### Example 1: Coding Agent (from Article)

```yaml
# Anthropic's Example
task:
  id: "fix-auth-bypass_1"
  graders:
    - type: deterministic_tests
      required: [test_empty_pw_rejected.py, test_null_pw_rejected.py]
    - type: llm_rubric
      rubric: prompts/code_quality.md
    - type: static_analysis
      commands: [ruff, mypy, bandit]
    - type: tool_calls
      required:
        - {tool: read_file, params: {path: "src/auth/*"}}
        - {tool: edit_file}
        - {tool: run_tests}
```

**Mapped to AEval:**
```json
{
  "scenario": "scn-007",
  "dataset": "ds-002",
  "agent": "ag-002",
  "metrics": [
    "met-023",  // Binary Test Pass Rate
    "met-027",  // LLM Rubric Score
    "met-024",  // Static Analysis Score
    "met-026"   // Tool Call Correctness
  ],
  "tracked_metrics": [
    {"type": "transcript", "metrics": ["met-041", "met-042", "met-043"]},
    {"type": "latency", "metrics": ["met-044", "met-045", "met-046"]}
  ]
}
```

---

### Example 2: Conversational Agent (from Article)

```yaml
# Anthropic's Example
graders:
  - type: llm_rubric
    assertions:
      - "Agent showed empathy for customer's frustration"
      - "Resolution was clearly explained"
      - "Agent's response grounded in fetch_policy tool results"
  - type: state_check
    expect:
      tickets: {status: resolved}
      refunds: {status: processed}
  - type: tool_calls
    required:
      - {tool: verify_identity}
      - {tool: process_refund, params: {amount: "<=100"}}
      - {tool: send_confirmation}
```

**Mapped to AEval:**
```json
{
  "scenario": "scn-006",
  "dataset": "ds-001",
  "agent": "ag-001",
  "metrics": [
    "met-027",  // LLM Rubric Score (empathy assertions)
    "met-025",  // Outcome Verification (state check)
    "met-026",  // Tool Call Correctness
    "met-041"   // Turn Count (transcript constraint)
  ]
}
```

---

## Part 9: Implementation Priority Matrix

### High Priority (Immediate Value)

| Item | Impact | Effort | Priority |
|------|--------|--------|----------|
| pass@k metrics (met-036, met-037, met-038) | High | Low | ⭐⭐⭐ |
| Transcript metrics (met-041 to met-046) | High | Low | ⭐⭐⭐ |
| LLM Rubric Score (met-027) | High | Medium | ⭐⭐⭐ |
| Multi-Turn Support scenario (scn-006) | High | Medium | ⭐⭐⭐ |
| Research Agent (ag-004) | Medium | Low | ⭐⭐ |

### Medium Priority (Expand Coverage)

| Item | Impact | Effort | Priority |
|------|--------|--------|----------|
| Code Refactoring scenario (scn-007) | Medium | Medium | ⭐⭐ |
| Research Synthesis scenario (scn-008) | Medium | Medium | ⭐⭐ |
| Static Analysis Score (met-024) | Medium | Low | ⭐⭐ |
| Tool Call Correctness (met-026) | Medium | Low | ⭐⭐ |
| Groundedness metrics (met-047 to met-050) | Medium | Medium | ⭐⭐ |

### Low Priority (Future Enhancement)

| Item | Impact | Effort | Priority |
|------|--------|--------|----------|
| Computer Use Agent (ag-005) | Low | High | ⭐ |
| Web Navigation scenario (scn-009) | Low | High | ⭐ |
| Human grader metrics (met-032 to met-035) | Low | High | ⭐ |
| Multi-Agent Orchestrator (ag-006) | Low | High | ⭐ |

---

## Part 10: Quick Reference Card

### Grader Selection Guide

```
┌─────────────────────────────────────────────────────────┐
│                  GRADER SELECTION GUIDE                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  What do you want to measure?                            │
│                                                          │
│  ┌─ Code/Format Validation ──────────────────────────┐   │
│  │ → Code-Based Graders (met-021 to met-026)        │   │
│  │   Fast, cheap, objective                          │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ Quality/Nuance ───────────────────────────────────┐   │
│  │ → Model-Based Graders (met-027 to met-031)        │   │
│  │   Flexible, scalable, requires calibration        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ Gold Standard/Complex Domain ─────────────────────┐   │
│  │ → Human Graders (met-032 to met-035)              │   │
│  │   Expensive, slow, expert quality                 │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ Reliability/Consistency ──────────────────────────┐   │
│  │ → pass@k / pass^k Metrics (met-036 to met-040)    │   │
│  │   Measure success probability                      │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ Process/Performance ───────────────────────────────┐   │
│  │ → Transcript Metrics (met-041 to met-046)         │   │
│  │   Track execution process                          │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Scenario Selection Guide

```
┌─────────────────────────────────────────────────────────┐
│                 SCENARIO SELECTION GUIDE                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Agent Type         → Recommended Scenario              │
│  ────────────────────────────────────────────────────   │
│  Coding             → scn-003, scn-007                   │
│  Conversational     → scn-001, scn-006                   │
│  RAG                → scn-002, scn-006                   │
│  Research           → scn-008                            │
│  Computer Use       → scn-009                            │
│  All (Safety)       → scn-004, scn-010                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0.0
**Created:** 2026-02-03
**Based on:** Anthropic Engineering - "Demystifying evals for AI agents"
**Status:** Complete Mapping
