"""
Council runner — Claude orchestrator with Claude subagents.
Usage: python run_council.py --council council_code_review.md --question "Review this code: ..."
       echo "Review this:" | python run_council.py --council council_code_review.md
"""

import anthropic
import argparse
import random
import string
import sys
import yaml
from pathlib import Path

MODEL = "claude-opus-4-6"
client = anthropic.Anthropic()


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
    """Parse a council config file and resolve SKILL.md personas."""
    council_path = Path(path)
    lines = council_path.read_text().splitlines()
    yaml_lines = [l for l in lines if not l.startswith("#")]
    config = yaml.safe_load("\n".join(yaml_lines))

    # Resolve SKILL.md paths relative to council file location
    base = council_path.parent
    config["MEMBERS"] = [
        load_skill(base / p) for p in config.get("PERSONAS", [])
    ]
    return config


# ── Stage 1: Independent responses ───────────────────────────────────────────

def stage1_independent(council: dict, question: str) -> dict[str, str]:
    """Ask each council member independently. Returns {member_name: response}."""
    responses = {}
    members = council["MEMBERS"]

    print(f"\n{'='*60}")
    print("STAGE 1 — Independent Responses")
    print(f"{'='*60}")

    for member in members:
        system = member["prompt"]  # full SKILL.md body is the system prompt

        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            thinking={"type": "adaptive"},
            system=system,
            messages=[{"role": "user", "content": question}],
        )
        text = next(b.text for b in resp.content if b.type == "text")
        responses[member["name"]] = text
        print(f"\n[{member['name']}]\n{text}")

    return responses


# ── Stage 2: Anonymized peer review ───────────────────────────────────────────

def stage2_peer_review(council: dict, question: str, responses: dict[str, str]) -> dict[str, str]:
    """Each member reviews anonymized responses. Returns {member_name: review}."""
    members = council["MEMBERS"]

    # Shuffle and assign labels
    names = list(responses.keys())
    random.shuffle(names)
    labels = list(string.ascii_uppercase[: len(names)])
    label_to_name = dict(zip(labels, names))

    labeled_block = "\n\n".join(
        f"**Response {label}:**\n{responses[name]}"
        for label, name in label_to_name.items()
    )

    print(f"\n{'='*60}")
    print("STAGE 2 — Anonymized Peer Review")
    print(f"Label mapping (hidden from agents): {label_to_name}")
    print(f"{'='*60}")

    reviews = {}
    for member in members:
        system = (
            member["prompt"] + "\n\n"
            "You are now in PEER REVIEW mode. You are evaluating anonymized responses.\n"
            "You do NOT know which response is yours.\n\n"
            "You MUST:\n"
            "1. Rank responses from most to least useful (format: '1: Response X — reason | 2: ...')\n"
            "2. Identify at least ONE flaw in the highest-ranked response\n"
            "3. Identify at least ONE thing you would change about the response closest to your perspective\n\n"
            "Disagreement is valued. Do NOT simply agree with the majority view."
        )

        user_msg = (
            f"**Original question:** {question}\n\n"
            f"**Anonymized responses to review:**\n\n{labeled_block}"
        )

        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            thinking={"type": "adaptive"},
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        text = next(b.text for b in resp.content if b.type == "text")
        reviews[member["name"]] = text
        print(f"\n[{member['name']} reviewing]\n{text}")

    return reviews, label_to_name


# ── Stage 3: Chairman synthesis ───────────────────────────────────────────────

def stage3_synthesize(council: dict, question: str, responses: dict, reviews: dict, label_to_name: dict) -> str:
    """Chairman synthesizes all responses and reviews into a final answer."""

    print(f"\n{'='*60}")
    print("STAGE 3 — Chairman Synthesis")
    print(f"{'='*60}")

    # Build context for chairman
    original_block = "\n\n".join(
        f"**{name}:**\n{resp}" for name, resp in responses.items()
    )
    review_block = "\n\n".join(
        f"**{name}'s review:**\n{rev}" for name, rev in reviews.items()
    )
    label_reveal = ", ".join(f"Response {l} = {n}" for l, n in label_to_name.items())

    system = (
        f"You are the Chairman of the {council['COUNCIL_NAME']} Council. "
        f"Your job is to synthesize a multi-agent deliberation into a final answer.\n\n"
        f"Your synthesis MUST:\n"
        f"1. State where all agents agreed (mark as HIGH CONFIDENCE)\n"
        f"2. State where agents disagreed and present both sides (mark as DISPUTED)\n"
        f"3. Incorporate the strongest unique points from each perspective\n"
        f"4. Be honest about what the council does NOT know or cannot resolve\n"
        f"5. If all agents agreed on something, note it but treat it with mild caution "
        f"(shared bias risk from same-model limitations)\n\n"
        f"Do NOT produce a watered-down average. Amplify the best insights, flag real disagreements."
    )

    user_msg = (
        f"**Question posed to the council:** {question}\n\n"
        f"**Label reveal:** {label_reveal}\n\n"
        f"**Original independent responses:**\n{original_block}\n\n"
        f"**Peer review feedback:**\n{review_block}"
    )

    resp = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )
    final = next(b.text for b in resp.content if b.type == "text")
    print(f"\n[FINAL SYNTHESIS]\n{final}")
    return final


# ── Main ─────────────────────────────────────────────────────────────────────

def run_council(council_path: str, question: str) -> str:
    council = load_council(council_path)

    print(f"\nCouncil: {council['COUNCIL_NAME']}")
    print(f"Members: {[m['name'] for m in council['MEMBERS']]}")
    print(f"Question: {question[:100]}{'...' if len(question) > 100 else ''}")

    responses = stage1_independent(council, question)
    reviews, label_to_name = stage2_peer_review(council, question, responses)
    final = stage3_synthesize(council, question, responses, reviews, label_to_name)
    return final


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--council", required=True, help="Path to council .md config")
    parser.add_argument("--question", default=None, help="Question to pose")
    args = parser.parse_args()

    question = args.question
    if not question:
        question = sys.stdin.read().strip()
    if not question:
        print("Provide a question via --question or stdin", file=sys.stderr)
        sys.exit(1)

    run_council(args.council, question)
