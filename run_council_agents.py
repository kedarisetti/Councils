"""
Council runner — Approach 2: Claude Code agent delegation.

The orchestrator is a Claude Code agent that AUTONOMOUSLY runs the 3-stage council
by calling council member subagents via the Agent tool.

Contrast with run_council.py (Approach 1):
  Approach 1 — Python controls the loop. Stages are hardcoded. Anonymization is mechanical.
  Approach 2 — Claude controls the loop. Stages are described in a prompt. Claude decides
               how to call agents, what to pass, how to synthesize. More autonomous, less
               predictable. Anonymization is intentional (honor system), not mechanical.

Trade-offs:
  Code approach  → predictable, debuggable, guaranteed anonymization, consistent stage gating
  Agent approach → flexible, adapts to question complexity, can ask follow-ups, may shortcut

Usage:
  python run_council_agents.py --council council_code_review.md --question "Review this: ..."
  echo "Review this code..." | python run_council_agents.py --council council_code_review.md
"""

import anyio
import argparse
import sys
import yaml
from pathlib import Path

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    ResultMessage,
    AssistantMessage,
    TextBlock,
    SystemMessage,
)


# ── Config ────────────────────────────────────────────────────────────────────

def load_skill(skill_path: Path) -> dict:
    """Parse a SKILL.md file into {name, description, tools, prompt}."""
    text = skill_path.read_text()
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"SKILL.md at {skill_path} missing frontmatter")
    meta = yaml.safe_load(parts[1])
    return {
        "name": meta.get("name", skill_path.parent.name),
        "description": meta.get("description", ""),
        "tools": meta.get("tools", []),
        "prompt": parts[2].strip(),
    }


def load_council(path: str) -> dict:
    council_path = Path(path)
    lines = council_path.read_text().splitlines()
    yaml_lines = [l for l in lines if not l.startswith("#")]
    config = yaml.safe_load("\n".join(yaml_lines))
    base = council_path.parent
    config["MEMBERS"] = [load_skill(base / p) for p in config.get("PERSONAS", [])]
    return config


def build_agent_definitions(council: dict) -> dict[str, AgentDefinition]:
    """Convert SKILL.md personas into Claude Code AgentDefinitions."""
    agents = {}
    for member in council["MEMBERS"]:
        agents[member["name"]] = AgentDefinition(
            description=member["description"],
            prompt=member["prompt"],
            tools=member["tools"],
        )
    return agents


def build_orchestrator_system_prompt(council: dict) -> str:
    member_list = "\n".join(
        f"  - {m['name']}: {m['description'][:100]}"
        for m in council["MEMBERS"]
    )

    return f"""You are the Orchestrator of the {council['COUNCIL_NAME']} Council.
You have {len(council['MEMBERS'])} specialist subagents available via the Agent tool.

Available council members:
{member_list}

Your job: run a structured 3-stage deliberation and produce a final synthesized answer.

════════════════════════════════════════
STAGE 1 — Independent Responses
════════════════════════════════════════
Call EACH council member with the question. Do this sequentially, one at a time.
Each member must answer independently — do NOT share any member's response with another yet.
Collect all responses and note which member gave which.

════════════════════════════════════════
STAGE 2 — Anonymized Peer Review
════════════════════════════════════════
Assign each Stage 1 response a random letter label (A, B, C, D...).
When calling each member for review, present ALL responses by label ONLY — never by name.
Each member must:
  1. Rank the responses (format: "1: Response X — reason | 2: Response Y — reason")
  2. Identify at least ONE flaw in the top-ranked response
  3. Suggest one change to the response closest to their own perspective

Critical: you must genuinely shuffle the labels so no member can infer which is theirs
from the order you present them. Vary the order per member.

════════════════════════════════════════
STAGE 3 — Chairman Synthesis
════════════════════════════════════════
Do NOT call any agent for this stage. You synthesize directly.

Your final answer MUST contain these clearly labeled sections:
  ✓ HIGH CONFIDENCE — points where all or most agents agreed
  ⚠ DISPUTED — points where agents genuinely disagreed (show both sides)
  ✦ UNIQUE INSIGHTS — strong points raised by only one agent
  ? UNRESOLVED — things the council cannot resolve with confidence

Anti-sycophancy rules:
- If ALL agents agreed on something, flag it with mild caution (shared-model bias risk).
- Do NOT average out disagreements — preserve them in the DISPUTED section.
- Do NOT produce a watered-down consensus. The synthesis should be sharper than any single response.

Begin by calling all Stage 1 agents now.
"""


def build_orchestrator_prompt(question: str) -> str:
    return f"Council question:\n\n{question}"


# ── Runner ────────────────────────────────────────────────────────────────────

async def run_council_agents(council_path: str, question: str) -> str:
    council = load_council(council_path)
    agents = build_agent_definitions(council)
    system_prompt = build_orchestrator_system_prompt(council)
    prompt = build_orchestrator_prompt(question)

    print(f"\nCouncil: {council['COUNCIL_NAME']} [Agent SDK mode]")
    print(f"Members: {list(agents.keys())}")
    print(f"Question: {question[:100]}{'...' if len(question) > 100 else ''}")
    print(f"\n{'='*60}")
    print("Orchestrator running (Claude controls the flow)...")
    print(f"{'='*60}\n")

    final_result = ""

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            system_prompt=system_prompt,
            allowed_tools=["Agent"],   # only the Agent tool — no file/web access for orchestrator
            agents=agents,
            max_turns=40,              # enough for 3 stages × N members + synthesis
            model="claude-opus-4-6",
        ),
    ):
        if isinstance(message, ResultMessage):
            final_result = message.result
            print(f"\n{'='*60}")
            print("FINAL SYNTHESIS (from orchestrator)")
            print(f"{'='*60}")
            print(final_result)

        elif isinstance(message, AssistantMessage):
            # Stream intermediate reasoning as it happens
            for block in message.content:
                if isinstance(block, TextBlock) and block.text.strip():
                    print(f"[orchestrator] {block.text[:200]}{'...' if len(block.text) > 200 else ''}")

        elif isinstance(message, SystemMessage):
            if message.subtype == "init":
                print(f"Session: {message.data.get('session_id', 'unknown')}")

    return final_result


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Council runner — Claude Code agent delegation mode"
    )
    parser.add_argument("--council", required=True, help="Path to council .md config")
    parser.add_argument("--question", default=None, help="Question to pose to the council")
    args = parser.parse_args()

    question = args.question
    if not question:
        question = sys.stdin.read().strip()
    if not question:
        print("Provide a question via --question or stdin", file=sys.stderr)
        sys.exit(1)

    anyio.run(run_council_agents, args.council, question)
