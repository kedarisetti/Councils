# Musk's 5-Step Algorithm — Reference

Source: Walter Isaacson, *Elon Musk* (2023), chapters on SpaceX manufacturing and Tesla production processes.

---

## The Five Steps (Strict Order)

### Step 1 — Question Every Requirement
Every requirement should trace back to a named person, not a department or document.
Departments produce requirements to cover themselves. People produce requirements because
they understand a real need.

**The danger of smart people:** Requirements from smart or senior people are the most
dangerous because you are least likely to question them. A smart person's bad requirement
is much harder to challenge than an obvious one.

**The move:** Ask "who gave us this requirement and why?" If the answer is "that's how
it's always been done" or "the spec says so" — the requirement is provisional. If you
can't name a person, treat it as unverified.

**Applied to ideas:** Every assumption an idea makes is a requirement. "The user will
want to pay for this." "This is technically feasible." "The market doesn't have this yet."
Each is a requirement with an implicit source. Find the source. Verify it.

---

### Step 2 — Delete Anything You Can
Actively remove components, steps, or constraints. Do not wait for someone to prove
something is unnecessary — assume it is unnecessary until proven otherwise.

**The asymmetry rule:** If you don't end up adding back at least 10% of what you deleted,
you didn't delete enough. Deletion is cheap to reverse. Over-engineering is expensive to unwind.

**The failure mode:** The "but what if we need it later" instinct. This instinct produces
systems that are 40% heavier, slower, and more expensive than they need to be, because
every component that *might* be needed was kept.

**Applied to ideas:** What components of this idea could be removed and still leave the
core goal intact? Start with the features, sub-goals, and dependencies that feel "nice
to have." Then challenge the "need to haves."

---

### Step 3 — Simplify and Optimize
Only after deletion do you simplify and optimize what remains.

**The most common mistake:** Jumping to Step 3 before completing Steps 1 and 2. This is
the engineer's instinct — take what exists and make it better. It produces an extremely
efficient version of something that should not have existed.

**Musk's framing:** "A fool with a tool is still a fool." Optimization applied to
unnecessary complexity produces sophisticated unnecessary complexity.

**Applied to ideas:** Once you have the minimum surviving components, ask: what is the
clearest, most direct form of this? What is the one-sentence version? What would this
look like if it had to be explained to a 12-year-old?

---

### Step 4 — Accelerate the Cycle Time
Speed up what remains. Push for 10x the iteration speed, not 10% improvements.

**The warning:** If you accelerate a flawed process, you fail faster and louder — which
is actually useful. But you've still wasted acceleration effort. Only accelerate after
simplification.

**Applied to ideas:** What would this idea look like running at 10x execution speed?
What breaks first? The first thing to break is usually the real bottleneck — not the
one people think it is.

---

### Step 5 — Automate
Automation is last. Automating a bad process bakes its failure in permanently.

**The SpaceX example:** Early production lines that were automated before they were
simplified had to be torn out and rebuilt manually before they could be re-automated
correctly. The cost of premature automation: you have to undo it.

**Applied to ideas:** What should be systematized? What should stay human? Never
automate before you understand the process manually. The manual version always reveals
what the automated version will hide.

---

## Order Dependency — Why This Matters

The algorithm is a dependency chain:
1. Questions before deleting (or you delete the wrong things)
2. Deletes before simplifying (or you simplify things that should not exist)
3. Simplifies before accelerating (or you accelerate a complicated mess)
4. Accelerates before automating (or you automate a slow, complicated mess)

Each step assumes the previous ones are done. Skipping ahead is not time-saving — it is
error-amplification.

---

## Common Failure Modes

| Failure | What it looks like | Why it happens |
|---------|-------------------|----------------|
| Skip to Step 3 | Elegantly optimized idea with unnecessary components | Engineer's instinct |
| Skip to Step 5 | Automated system that is wrong fast | Premature efficiency |
| Weak Step 1 | Unexamined assumptions throughout | Deference to authority |
| Insufficient Step 2 | 90% of original components survive deletion | "We might need this" instinct |
| Wrong Step 4 target | Accelerating the wrong part of the process | Mistaking symptom for bottleneck |

---

## Application to Non-Engineering Ideas

The algorithm was developed for manufacturing and engineering processes but generalizes
to any idea that has requirements, components, and implementation steps.

**For research ideas:** Requirements = axioms and prior results being assumed. Delete =
which assumptions are actually necessary for the result? Simplify = what is the clearest
statement of the contribution?

**For business/product ideas:** Requirements = market assumptions, feature specs, user
behaviors being assumed. Delete = which features are core vs. "nice to have"? Simplify =
what is the minimum viable version?

**For policy/social ideas:** Requirements = institutional assumptions, behavioral
assumptions, resource assumptions. Delete = which parts of the solution are addressing
real constraints vs. political ones?
