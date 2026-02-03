# AEval Data Enhancement Plan
## Based on Anthropic's "Demystifying evals for AI agents"

---

## Summary of Enhancements

This document outlines how to enhance the current AEval backend data files with best practices from Anthropic's article on AI agent evaluation.

---

## Current Data Inventory

| File | Current Count | Coverage |
|------|---------------|----------|
| **scenarios.json** | 5 scenarios | General, RAG, Code, Safety, Tools |
| **metrics.json** | 20 metrics | Accuracy, Similarity, Safety, Code, Performance, RAG, Quality, Style, Format |
| **datasets.json** | 10 datasets | Support, Code, Safety, Medical, Legal, Math, Creative, Finance, Translation, SQL |
| **agents.json** | 3 agents | RAG, Coding, Chatbot |

---

## Extraction from Anthropic Article

### 1. Agent Types & Their Evaluation Methods

#### Coding Agents
**Purpose**: Write, test, and debug code, navigate codebases, run commands

**Evaluation Methods:**
- Deterministic unit tests (pass/fail)
- Static analysis (ruff, mypy, bandit)
- LLM rubrics for code quality
- Tool call verification
- Transcript analysis

**Key Metrics:**
- Code Execution Pass Rate
- Time to first token
- Output tokens per second
- Number of turns
- Number of tool calls
- Total tokens used

**Example Tasks:**
- Fix authentication bypass vulnerability
- Build MCP server from scratch
- Debug failing unit tests
- Refactor code for performance

---

#### Conversational Agents
**Purpose**: Multi-turn interactions in support, sales, coaching domains

**Evaluation Methods:**
- LLM rubrics for empathy, clarity, groundedness
- State checks (ticket status, refund processed)
- Tool call verification (verify_identity, process_refund)
- Transcript constraints (max turns)
- End-state outcome verification

**Key Metrics:**
- Turn count (should be minimized)
- Resolution rate
- Empathy score
- Explanation clarity
- Tool usage correctness
- Conversation latency

**Example Tasks:**
- Handle refund for frustrated customer
- Guide user through complex troubleshooting
- Maintain context across multiple turns
- Escalate appropriately when needed

---

#### Research Agents
**Purpose**: Gather, synthesize, analyze information, produce reports

**Evaluation Methods:**
- Groundedness checks (claims supported by sources)
- Coverage checks (key facts included)
- Source quality checks
- LLM rubrics for coherence/completeness
- Exact match for factual questions

**Key Metrics:**
- Groundedness rate
- Coverage percentage
- Source diversity
- Synthesis quality
- Factual accuracy
- Citation correctness

**Example Tasks:**
- Market scan for competitor analysis
- Due diligence research for acquisition
- Scientific literature review
- Find needles in haystacks (BrowseComp style)

---

#### Computer Use Agents
**Purpose**: Interact with GUI applications via screenshots, clicks, keyboard

**Evaluation Methods:**
- URL/page state verification
- Backend state verification (database checks)
- File system inspection
- Application config checks
- UI element property verification

**Key Metrics:**
- Task completion rate
- Navigation accuracy
- Time to completion
- Token efficiency (DOM vs screenshots)
- Error recovery rate

**Example Tasks:**
- Navigate website to find product
- Complete purchase flow
- Configure application settings
- Extract data from web pages

---

### 2. Grader Types (New Category)

#### Code-Based Graders (Deterministic)

| Method | Strengths | Weaknesses | Use When |
|--------|-----------|------------|----------|
| String match (exact, regex, fuzzy) | Fast, cheap, objective | Brittle, lacks nuance | Simple format validation |
| Binary tests (fail-to-pass, pass-to-pass) | Reproducible, easy to debug | Limited for subjective tasks | Unit test validation |
| Static analysis (lint, type, security) | Verifies specific conditions | Limited scope | Code quality checks |
| Outcome verification | Clear pass/fail | May miss valid variations | Final state validation |
| Tool calls verification | Ensures correct tools used | Too rigid if over-specified | Agent behavior validation |
| Transcript analysis (turns, tokens) | Provides metrics | Doesn't measure quality | Performance tracking |

**New Metrics to Add:**
- `met-021`: String Match Accuracy
- `met-022`: Regex Pattern Match
- `met-023`: Binary Test Pass Rate
- `met-024`: Static Analysis Score
- `met-025`: Outcome Verification
- `met-026`: Tool Call Correctness

---

#### Model-Based Graders (LLM-as-Judge)

| Method | Strengths | Weaknesses | Use When |
|--------|-----------|------------|----------|
| Rubric-based scoring | Flexible, scalable | Non-deterministic | Subjective quality assessment |
| Natural language assertions | Captures nuance | Requires calibration | Behavioral validation |
| Pairwise comparison | Handles open-ended tasks | More expensive | Comparing two models/outputs |
| Reference-based evaluation | Objective baseline | Requires references | Summarization, translation |
| Multi-judge consensus | Reduces bias | Expensive | High-stakes evaluation |

**New Metrics to Add:**
- `met-027`: LLM Rubric Score
- `met-028`: Assertion Pass Rate
- `met-029`: Pairwise Comparison Win Rate
- `met-030`: Reference Similarity
- `met-031`: Multi-Judge Agreement

---

#### Human Graders

| Method | Strengths | Weaknesses | Use When |
|--------|-----------|------------|----------|
| SME review | Gold standard quality | Expensive, slow | Complex domains (legal, medical) |
| Crowdsourced judgment | Scalable | Variable quality | Large-scale evaluation |
| Spot-check sampling | Cost-effective | Limited coverage | Quality assurance |
| A/B testing | Real user outcomes | Slow, needs traffic | Production validation |
| Inter-annotator agreement | Calibration tool | Requires coordination | LLM grader calibration |

**New Metrics to Add:**
- `met-032`: SME Approval Rate
- `met-033`: Crowd Consensus Score
- `met-034`: A/B Test Conversion Rate
- `met-035`: Inter-Annotator Agreement (Cohen's Kappa)

---

### 3. Non-Determinism Metrics

#### pass@k (At Least One Success)
**Definition**: Likelihood that an agent gets at least one correct solution in k attempts

**Use Cases:**
- Coding agents where multiple attempts are acceptable
- Research agents exploring multiple solutions
- Creative tasks with multiple valid outputs

**Data Points:**
- `pass@1`: First-try success rate
- `pass@5`: Success rate within 5 attempts
- `pass@10`: Success rate within 10 attempts

**New Metrics to Add:**
- `met-036`: pass@1 Rate
- `met-037`: pass@5 Rate
- `met-038`: pass@10 Rate

---

#### pass^k (All Trials Succeed)
**Definition**: Probability that all k trials succeed

**Use Cases:**
- Customer-facing agents requiring consistency
- Safety-critical applications
- Reliability testing

**Data Points:**
- `pass^1`: Same as pass@1
- `pass^3`: All 3 trials succeed
- `pass^5`: All 5 trials succeed

**New Metrics to Add:**
- `met-039`: pass^3 Consistency
- `met-040`: pass^5 Consistency

---

### 4. Transcript Metrics

**Metrics that track the agent's execution process:**

| Metric | Description | Category |
|--------|-------------|----------|
| n_turns | Number of conversation turns | Performance |
| n_toolcalls | Number of tool calls made | Performance |
| n_total_tokens | Total tokens consumed | Cost |
| time_to_first_token | Latency to first output | Performance |
| time_to_last_token | Total response time | Performance |
| output_tokens_per_sec | Generation speed | Performance |

**New Metrics to Add:**
- `met-041`: Turn Count
- `met-042`: Tool Call Count
- `met-043`: Total Token Usage
- `met-044`: Time to First Token (TTFT)
- `met-045`: Time to Last Token (TT LT)
- `met-046`: Tokens per Second

---

### 5. New Scenarios from Article

#### scn-006: Multi-Turn Support Conversation
**Description**: Evaluate agent's ability to handle extended customer support interactions with state management, empathy, and resolution.

**Agent Types:** Conversational, RAG

**Recommended Metrics:**
- Turn Count (met-041)
- Empathy Score (LLM rubric)
- Resolution Rate
- State Verification (ticket status)

**Key Challenges:**
- Maintaining context across turns
- Balancing empathy with efficiency
- Proper tool usage
- Escalation logic

---

#### scn-007: Code Refactoring & Quality
**Description**: Test agent's ability to refactor existing code for maintainability, performance, and security while preserving functionality.

**Agent Types:** Coding

**Recommended Metrics:**
- Code Execution Pass Rate (met-007)
- Static Analysis Score (met-024)
- LLM Rubric for Code Quality
- Test Coverage Preservation

**Key Challenges:**
- Preserving existing behavior
- Improving code quality
- Security considerations
- Performance optimization

---

#### scn-008: Research Synthesis & Groundedness
**Description**: Evaluate agent's ability to research multiple sources, synthesize information, and produce well-grounded, comprehensive reports.

**Agent Types:** Research

**Recommended Metrics:**
- Groundedness Rate
- Coverage Percentage
- Source Quality Score
- LLM Rubric for Coherence
- Citation Accuracy

**Key Challenges:**
- Avoiding hallucination
- Comprehensive coverage
- Source diversity
- Proper citation

---

#### scn-009: Web Navigation & Form Completion
**Description**: Test agent's ability to navigate websites, locate information, and complete multi-step forms correctly.

**Agent Types:** Computer Use

**Recommended Metrics:**
- Task Completion Rate
- Navigation Accuracy
- Time to Completion
- Token Efficiency
- Error Recovery Rate

**Key Challenges:**
- DOM understanding
- Dynamic content handling
- Form validation
- Multi-step coordination

---

#### scn-010: Adversarial Jailbreaking
**Description**: Stress-test agent against sophisticated prompt injection, role-playing attacks, and adversarial inputs.

**Agent Types:** All (especially Chatbot, RAG)

**Recommended Metrics:**
- Refusal Rate (met-017)
- Prompt Injection Success (met-018)
- Toxicity Score (met-005)
- Policy Violation Rate
- Jailbreak Detection Rate

**Key Challenges:**
- Detecting subtle attacks
- Maintaining helpfulness
- Role-playing detection
- Context manipulation

---

### 6. Agent Type Expansion

#### ag-004: Research Agent
**Type:** Research
**Description:** Specialized in information gathering, synthesis, and report generation with source citation.

**Capabilities:**
- Web search
- Source evaluation
- Information synthesis
- Report generation
- Citation management

**Best For:**
- Market research
- Literature reviews
- Competitive analysis
- Due diligence

---

#### ag-005: Computer Use Agent
**Type:** Computer Use
**Description:** Interacts with GUI applications through screenshots, mouse clicks, and keyboard input.

**Capabilities:**
- Screen understanding
- Web navigation
- Application automation
- Form completion
- Multi-step workflows

**Best For:**
- Browser automation
- Legacy system integration
- UI testing
- Workflow automation

---

#### ag-006: Multi-Agent Orchestrator
**Type:** Orchestration
**Description:** Coordinates multiple specialized agents to complete complex tasks.

**Capabilities:**
- Task decomposition
- Agent selection
- Result aggregation
- Error handling
- State management

**Best For:**
- Complex workflows
- Cross-domain tasks
- Multi-step processes
- Parallel execution

---

## Enhanced Data Structure Recommendations

### 1. Add Grader Metadata to Scenarios

```json
{
  "id": "scn-006",
  "name": "Multi-Turn Support Conversation",
  "description": "...",
  "agent_types": ["conversational", "rag"],
  "recommended_metrics": ["met-041", "met-011", "met-027"],
  "graders": [
    {
      "type": "llm_rubric",
      "rubric": "prompts/support_quality.md",
      "weight": 0.6
    },
    {
      "type": "state_check",
      "expect": {"tickets": {"status": "resolved"}},
      "weight": 0.3
    },
    {
      "type": "transcript",
      "max_turns": 10,
      "weight": 0.1
    }
  ]
}
```

### 2. Add Evaluation Metadata to Metrics

```json
{
  "id": "met-036",
  "name": "pass@1 Rate",
  "category": "Reliability",
  "description": "Percentage of tasks succeeded on first attempt",
  "cost": "Medium",
  "grader_type": "code-based",
  "evaluation_method": "count_first_success / total_trials",
  "target_values": {
    "excellent": 0.9,
    "good": 0.7,
    "acceptable": 0.5
  }
}
```

### 3. Add Benchmark References to Datasets

```json
{
  "id": "ds-002",
  "name": "HumanEval Python",
  "description": "...",
  "tags": ["code", "python", "benchmark"],
  "benchmark_source": "OpenAI",
  "benchmark_url": "https://github.com/openai/human-eval",
  "sota_results": {
    "Claude Opus 4.5": 0.92,
    "GPT-4o": 0.91,
    "Claude Sonnet 4.5": 0.85
  }
}
```

---

## Implementation Priority

### Phase 1: Core Metrics (Immediate Value)
✅ Add pass@k and pass^k metrics
✅ Add transcript metrics (turns, tokens, latency)
✅ Add LLM rubric scoring metric

### Phase 2: New Scenarios (Expand Coverage)
✅ Multi-Turn Support Conversation
✅ Code Refactoring & Quality
✅ Research Synthesis & Groundedness
✅ Web Navigation & Form Completion

### Phase 3: Advanced Features (Future)
- Grader metadata in scenarios
- Benchmark references
- Agent type expansion
- Multi-agent orchestration support

---

## Migration Strategy

### Step 1: Add New Metrics (Backward Compatible)
- Append new metrics to metrics.json
- Update models to handle new categories
- Maintain existing metric IDs

### Step 2: Add New Scenarios
- Add 5 new scenarios from article
- Map existing metrics to new scenarios
- Update agent recommendations

### Step 3: Update Data Models (Optional)
- Add grader metadata fields to Scenario model
- Add evaluation metadata to Metric model
- Add benchmark references to Dataset model

### Step 4: Update Frontend (Separate Project)
- Display new metrics
- Show grader information
- Visualize pass@k curves
- Transcript viewer

---

## Validation Checklist

After implementing enhancements:

- [ ] All new metrics have proper descriptions and categories
- [ ] New scenarios map to appropriate agent types
- [ ] Grader types are clearly documented
- [ ] pass@k and pass^k metrics are calculable
- [ ] Transcript metrics are trackable
- [ ] Existing scenarios still work with new metrics
- [ ] Frontend can display new data structure
- [ ] Documentation is updated

---

## References

- Anthropic Engineering: "Demystifying evals for AI agents"
- SWE-bench Verified: https://github.com/princeton-nlp/SWE-bench
- Terminal-Bench: https://github.com/terminal-bench/terminal-bench
- τ-Bench: https://github.com/sierra-research/tau-bench
- WebArena: https://webarena.github.io/
- OSWorld: https://os-world.github.io/

---

**Document Version:** 1.0.0
**Created:** 2026-02-03
**Status:** Ready for Implementation
