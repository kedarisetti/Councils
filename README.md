# Council of Agents

A multi-agent deliberation system with three execution approaches. All three share the same
council config files and persona SKILL.md definitions — only the harness changes.

---

## Directory structure

```
councils/
├── CLAUDE.md                          ← Approach 3: orchestrator brain for native Claude Code
├── council_code_review.md             ← council config (shared by all approaches)
├── run_council.py                     ← Approach 1: Python controls the loop
├── run_council_agents.py              ← Approach 2: Python launches Claude as orchestrator
│
└── personas/
    ├── security-auditor/
    │   └── SKILL.md                   ← full persona: mindset, frameworks, output format, guardrails
    ├── performance-engineer/
    │   └── SKILL.md
    ├── maintainability-critic/
    │   └── SKILL.md
    └── domain-expert/
        └── SKILL.md
```

---

## How the 3-stage council works

Every approach runs the same logical process:

```
Stage 1 — Independent
  Each persona answers the question alone, with no visibility into other responses.
  This prevents anchoring — each brings their full expertise without being pulled
  toward a consensus before one has formed.

Stage 2 — Anonymized Peer Review
  Responses are shuffled and labeled A/B/C/D (identity hidden).
  Each persona reviews ALL labeled responses and must:
    1. Rank them
    2. Find at least one flaw in the top-ranked response
    3. Suggest one change to the response closest to their own perspective
  Forced dissent combats sycophancy. Anonymization prevents favoritism.

Stage 3 — Chairman Synthesis
  The orchestrator (not a persona) synthesizes across all responses and reviews.
  Output is structured as:
    ✓ HIGH CONFIDENCE  — where agents agreed
    ⚠ DISPUTED        — genuine disagreements, both sides shown
    ✦ UNIQUE INSIGHTS  — strong points from only one agent
    ? UNRESOLVED       — things the council cannot resolve
```

---

## Approach 1 — Python-controlled loop (`run_council.py`)

**What it is:** Python is the orchestrator. It calls the Anthropic API directly for each
stage, shuffles labels mechanically, and hardcodes the stage sequence.

```
Python
  ├── calls Anthropic API → persona A response
  ├── calls Anthropic API → persona B response
  ├── calls Anthropic API → persona C response     Stage 1
  ├── calls Anthropic API → persona D response
  │
  ├── shuffles labels [A→C, B→A, C→D, D→B]        (mechanical, guaranteed)
  ├── calls Anthropic API → persona A review
  ├── calls Anthropic API → persona B review        Stage 2
  ├── calls Anthropic API → persona C review
  ├── calls Anthropic API → persona D review
  │
  └── calls Anthropic API → chairman synthesis      Stage 3
```

**Run:**
```bash
python run_council.py --council council_code_review.md --question "Review: def divide(a,b): return a/b"
```

**When to use:**
- Production pipelines — deterministic, debuggable, exact API call count
- When you need guaranteed stage gating and mechanical anonymization
- Cost control — you know exactly what you're spending before you run it

---

## Approach 2 — Claude as orchestrator via Agent SDK (`run_council_agents.py`)

**What it is:** Python launches a Claude Code orchestrator session. Claude then autonomously
runs the council by calling persona subagents via the Agent tool. Each subagent is a separate
isolated Claude Code process running the full SKILL.md prompt.

```
Python
  └── launches Claude orchestrator (Agent SDK)
        └── Claude reads orchestrator system prompt, decides how to proceed
              ├── Agent tool → security-auditor subagent (isolated Claude process)
              ├── Agent tool → performance-engineer subagent (isolated Claude process)
              ├── Agent tool → maintainability-critic subagent (isolated Claude process)  Stage 1
              ├── Agent tool → domain-expert subagent (isolated Claude process)
              │
              ├── Claude shuffles labels internally (intentional, not mechanical)
              ├── Agent tool → each subagent for review                                   Stage 2
              │
              └── Claude synthesizes directly                                             Stage 3
```

**Run:**
```bash
python run_council_agents.py --council council_code_review.md --question "Review: def divide(a,b): return a/b"
```

**When to use:**
- Exploratory or research questions — Claude can adapt (ask follow-ups, weight members differently)
- When the orchestration logic itself should be flexible
- Testing how Claude interprets and executes the council process

**Key difference from Approach 1:** Anonymization is intentional (Claude is instructed to shuffle)
not mechanical (Python shuffles). Stage sequence is described, not hardcoded — Claude may adapt it.

---

## Approach 3 — Native Claude Code (`CLAUDE.md`)

**What it is:** No Python, no runner script. You open a `claude` session in the `councils/`
directory. Claude reads `CLAUDE.md` and becomes the orchestrator natively. It uses the Agent
tool to call persona subagents by reading their SKILL.md files directly.

```
User runs: claude (in councils/ directory)
  └── Claude reads CLAUDE.md → knows it's a council orchestrator
        └── User says: "Run the code review council on: ..."
              ├── Claude reads council_code_review.md → gets persona list
              ├── Claude reads each personas/*/SKILL.md → gets prompt + tools
              │
              ├── Agent tool → security-auditor (prompt = SKILL.md body)
              ├── Agent tool → performance-engineer                          Stage 1
              ├── Agent tool → maintainability-critic
              ├── Agent tool → domain-expert
              │
              ├── Claude assembles anonymized review prompts
              ├── Agent tool → each persona for review                       Stage 2
              │
              └── Claude synthesizes directly                                Stage 3
```

**Run:**
```bash
cd /path/to/councils
claude
# Then say: "Run the code review council on: def divide(a, b): return a/b"
```

**When to use:**
- Interactive use — you want to converse with the orchestrator, ask follow-ups, guide the process
- When you want Claude to decide which personas to call based on the question
- Building and sharpening council prompts iteratively

---

## Comparison

| Property                   | Approach 1 (Python loop) | Approach 2 (Agent SDK) | Approach 3 (Native Claude) |
|----------------------------|--------------------------|------------------------|----------------------------|
| **Orchestrator**           | Python                   | Claude (via SDK)       | Claude (native)            |
| **Stage enforcement**      | Guaranteed               | Instructed             | Instructed                 |
| **Anonymization**          | Mechanical (Python)      | Intentional (Claude)   | Intentional (Claude)       |
| **Subagent isolation**     | No (same API context)    | Yes (subprocess)       | Yes (subprocess)           |
| **API call count**         | Exact: N×2 + 1           | Variable               | Variable                   |
| **Persona definition**     | SKILL.md                 | SKILL.md               | SKILL.md                   |
| **Requires Python**        | Yes                      | Yes                    | No                         |
| **Interactive**            | No                       | No                     | Yes                        |
| **Best for**               | Production               | Autonomous research    | Iterative development      |

---

## Shared config: how personas are defined

All three approaches use the same `SKILL.md` format (from the
[persona_agents](https://github.com/doraemonyaki-19/persona_agents) pattern):

```markdown
---
name: security-auditor
description: One-line description of when to invoke this persona
tools:
  - Read
  - WebSearch
---

# Persona Name

Full system prompt: mindset, frameworks, what to check,
communication style, output format, guardrails.
```

Council configs reference persona paths:

```yaml
COUNCIL_NAME: "Code Review"
PERSONAS:
  - personas/security-auditor/SKILL.md
  - personas/performance-engineer/SKILL.md
  - personas/maintainability-critic/SKILL.md
  - personas/domain-expert/SKILL.md
```

---

## Creating a new council

1. Copy and rename `council_code_review.md`
2. Copy and customize personas from `personas/` or write new ones
3. Run with any of the three approaches — same config works for all

---

## Known limitations (all approaches)

- **Same base model = shared biases.** All agents run on Claude. Unanimous agreement
  carries echo chamber risk — the synthesis flags this explicitly.
- **Sycophancy grows with rounds.** Keep peer review to 1 round.
- **For maximum quality:** Swap different LLMs per persona in Approach 1 by changing
  the `MODEL` variable per member.
