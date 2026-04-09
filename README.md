# Council of Agents

A multi-agent deliberation system where multiple AI personas with distinct analytical
frameworks debate a question and a chairman synthesizes the result. Three execution
approaches share the same council configs and persona SKILL.md definitions — only the
harness changes.

---

## Councils

### Ideas Council (`council_ideas.md`)
Multi-domain idea evaluation. Works for product, research, mathematics, finance, or
policy. Designed to sharpen ideas rather than redirect them.

| Persona | Analytical Lens | Core Question |
|---------|----------------|---------------|
| **Reductionist** | Musk's 5-step algorithm | What's load-bearing vs. accretion? What is the minimum viable core? |
| **Adjacent Possible** | Steven Johnson — timing + purpose | Is this inside the current adjacent possible? Is it worth the world's time? |
| **Devil's Advocate** | Steelman opposition | What is the strongest case *against* this idea? |
| **Remarkability Analyst** | Godin's Purple Cow (domain-adapted) | Will this propagate — will people remark on it, cite it, build on it? |
| **Systems Thinker** | Second/third-order effects | What does success create? What does the world look like in 20 years if this wins? |

**Run:**
```
cd /path/to/councils && claude
> Run the ideas council on: I want to build a peer-to-peer local sync engine for notes — no server, CRDTs for conflict resolution. Should I pursue this?
> Run the ideas council on: I have a conjecture that prime gaps follow a log-normal distribution. Is this worth pursuing?
> Run the ideas council on: A policy idea — give every public school student a $500 annual "learning budget" to spend on any educational resource, no restrictions.
```

---

### Financial Investments Council (`council_financial_investments.md`)
Deep investment analysis across value fundamentals, quantitative signals, macro context,
risk stress-testing, and tail risk.

| Persona | Analytical Lens | Core Question |
|---------|----------------|---------------|
| **Value Investor** | Graham/Buffett — moat, owner earnings, margin of safety | Is this a great business at a fair price? |
| **Quant Analyst** | Factor models — value, momentum, quality, low-vol | What do the systematic signals say? |
| **Macro Strategist** | Top-down cycle analysis | How does the macro environment affect this investment? |
| **Risk Skeptic** | Fundamental bear analysis | What does the bear case look like? What assumption breaks the thesis? |
| **Tail Risk / Antifragility** | Full Taleb framework | Is this fragile, robust, or antifragile? Where is the hidden tail exposure? |

**Run:**
```
cd /path/to/councils && claude
> Run the financial investments council on: NVIDIA (NVDA) at current price — is the AI infrastructure thesis still intact or is this peak cycle?
> Run the financial investments council on: I'm considering a 10% allocation to long-dated US Treasuries as a tail hedge. Evaluate.
> Run the financial investments council on: Uranium miners ETF (URA) — nuclear energy renaissance thesis.
```

---

### Code Review Council (`council_code_review.md`)
Systematic code review across security, performance, maintainability, and domain correctness.

| Persona | Analytical Lens | Core Question |
|---------|----------------|---------------|
| **Security Auditor** | OWASP, exploit-first mindset | What can be exploited or abused? |
| **Performance Engineer** | Big-O, N+1, memory, concurrency | Where are the performance cliffs? |
| **Maintainability Critic** | Future-reader focus | Will the next engineer understand and safely modify this? |
| **Domain Expert** | Correctness and edge cases | Is this doing what it's supposed to do? |

**Run:**
```
cd /path/to/councils && claude
> Run the code review council on: def divide(a, b): return a/b
> Run the code review council on: [paste a function or file]
> Council: council_code_review.md — review the authentication module in auth/session.py
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

## Directory structure

```
councils/
├── CLAUDE.md                                    ← Approach 3: orchestrator brain for native Claude Code
├── council_ideas.md                             ← Ideas council config
├── council_financial_investments.md             ← Financial investments council config
├── council_code_review.md                       ← Code review council config
├── run_council.py                               ← Approach 1: Python controls the loop
├── run_council_agents.py                        ← Approach 2: Python launches Claude as orchestrator
│
└── personas/
    │
    │   # Ideas council
    ├── reductionist/
    │   ├── SKILL.md
    │   └── references/musk_algorithm.md
    ├── adjacent-possible/
    │   ├── SKILL.md
    │   └── references/johnson_concepts.md
    ├── devil-advocate/
    │   └── SKILL.md
    ├── remarkability-analyst/
    │   ├── SKILL.md
    │   └── references/remarkability_concepts.md
    ├── systems-thinker/
    │   └── SKILL.md
    │
    │   # Financial investments council
    ├── value-investor/
    │   └── SKILL.md
    ├── quant-analyst/
    │   └── SKILL.md
    ├── macro-strategist/
    │   └── SKILL.md
    ├── risk-skeptic/
    │   └── SKILL.md
    └── tail-risk-antifragility/
        ├── SKILL.md
        └── references/taleb_concepts.md
    │
    │   # Code review council
    ├── security-auditor/
    │   └── SKILL.md
    ├── performance-engineer/
    │   └── SKILL.md
    ├── maintainability-critic/
    │   └── SKILL.md
    └── domain-expert/
        └── SKILL.md
```

---

## Three execution approaches

### Approach 1 — Python-controlled loop (`run_council.py`)

Python is the orchestrator. It calls the Anthropic API directly for each stage, shuffles
labels mechanically, and hardcodes the stage sequence.

```
Python
  ├── calls Anthropic API → persona A response
  ├── calls Anthropic API → persona B response     Stage 1
  ├── calls Anthropic API → persona C response
  │
  ├── shuffles labels [A→C, B→A, C→B]              (mechanical, guaranteed)
  ├── calls Anthropic API → persona A review        Stage 2
  ├── calls Anthropic API → persona B review
  ├── calls Anthropic API → persona C review
  │
  └── calls Anthropic API → chairman synthesis      Stage 3
```

**Run:**
```bash
python run_council.py --council council_ideas.md --question "Should we build X?"
```

**When to use:** Production pipelines — deterministic, debuggable, exact API call count.
Guaranteed stage gating and mechanical anonymization. Supports any LLM per persona
(set `model` per member for heterogeneous councils).

---

### Approach 2 — Claude as orchestrator via Agent SDK (`run_council_agents.py`)

Python launches a Claude orchestrator session. Claude autonomously runs the council by
calling persona subagents via the Agent tool. Each subagent is a separate isolated
Claude Code process running the full SKILL.md prompt.

```
Python
  └── launches Claude orchestrator (Agent SDK)
        └── Claude reads orchestrator system prompt
              ├── Agent tool → persona A subagent (isolated Claude process)
              ├── Agent tool → persona B subagent (isolated Claude process)  Stage 1
              ├── Agent tool → persona C subagent (isolated Claude process)
              │
              ├── Claude shuffles labels (intentional, not mechanical)
              ├── Agent tool → each subagent for review                      Stage 2
              │
              └── Claude synthesizes directly                                Stage 3
```

**Run:**
```bash
python run_council_agents.py --council council_ideas.py --question "Should we build X?"
```

**When to use:** Exploratory or research questions — Claude can adapt the orchestration,
weight members differently, ask follow-ups. Testing how Claude interprets the council process.

---

### Approach 3 — Native Claude Code (`CLAUDE.md`)

No Python, no runner script. Open a `claude` session in the `councils/` directory. Claude
reads `CLAUDE.md` and becomes the orchestrator. Uses the Agent tool to call persona
subagents by reading their SKILL.md files.

```
User runs: claude (in councils/ directory)
  └── Claude reads CLAUDE.md → becomes council orchestrator
        └── User: "Run the ideas council on: ..."
              ├── Claude reads council_ideas.md → gets persona list
              ├── Claude reads each SKILL.md → gets prompt + tools
              │
              ├── Agent tool → reductionist subagent
              ├── Agent tool → adjacent-possible subagent              Stage 1
              ├── Agent tool → devil-advocate subagent
              │
              ├── Claude assembles anonymized review prompts
              ├── Agent tool → each persona for review                 Stage 2
              │
              └── Claude synthesizes directly                          Stage 3
```

**Run:**
```bash
cd /path/to/councils
claude
# Then: "Run the ideas council on: should we build a local-first sync engine?"
```

**When to use:** Interactive use — converse with the orchestrator, ask follow-ups, guide
the process. Iterative council and persona development.

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
| **Multi-LLM per persona**  | Yes (Approach 1 only)    | No                     | No                         |
| **Best for**               | Production               | Autonomous research    | Iterative development      |

---

## SKILL.md format

All three approaches use the same persona format:

```markdown
---
name: reductionist
description: One-line description of when to invoke this persona
tools:
  - Read
  - WebSearch
---

# Persona Name

Full system prompt: mindset, philosophy, analytical framework,
communication style, output format, guardrails.

May include a references/ subdirectory with domain concept docs
loadable via the Read tool.
```

Council configs reference persona paths:

```yaml
COUNCIL_NAME: "Ideas"
PERSONAS:
  - personas/reductionist/SKILL.md
  - personas/adjacent-possible/SKILL.md
  - personas/devil-advocate/SKILL.md
  - personas/remarkability-analyst/SKILL.md
  - personas/systems-thinker/SKILL.md
```

---

## Creating a new council

1. Create a new `council_<name>.md` with `COUNCIL_NAME` and a `PERSONAS` list
2. Write or copy persona SKILL.md files into `personas/<name>/`
3. Optionally add `references/` subdirectories with domain concept docs
4. Run with any of the three approaches — same config works for all

**Persona design principles:**
- Use expertise-based diversity (distinct analytical frameworks) over personality diversity
- Each persona should naturally conflict with at least one other on specific questions
- Include explicit conflict declarations in each SKILL.md so tension is productive
- Add a mandatory "what would change my mind" or "survivability" section to prevent pure nihilism
- Reference docs in `references/` keep SKILL.md focused while making depth available

---

## Known limitations

- **Same base model = shared biases.** All agents run on Claude. Unanimous agreement
  carries echo chamber risk — the synthesis flags this explicitly.
- **Sycophancy grows with rounds.** Keep peer review to 1 round.
- **For maximum epistemic diversity:** Use Approach 1 with different models per persona
  (Claude, GPT-4, Gemini via OpenRouter) — different training data reduces correlated errors.
