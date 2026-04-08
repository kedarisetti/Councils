# Taleb Core Concepts — Reference

## Antifragility
Beyond resilience. Three categories:
- **Fragile**: wants calm and predictability. Harmed by volatility. (Porcelain, over-leveraged balance sheets, businesses dependent on stable supply chains)
- **Robust/Resilient**: indifferent to volatility. (Rocks, cash, essential monopolies)
- **Antifragile**: gains from volatility, disorder, stress. (Evolution, options, businesses that absorb competitor failures)

Test: "What happens to this investment when conditions get turbulent and unpredictable?" If it breaks → fragile. If nothing → robust. If it gets stronger → antifragile.

---

## Ergodicity
The most important concept most investors ignore.

**Ensemble probability**: average outcome across 1000 parallel investors at one point in time.
**Time probability**: average outcome for one investor across 1000 time periods.

These are equal ONLY in ergodic systems (e.g. coin flips). Financial markets are NOT ergodic.

Why it matters: A strategy with positive expected value can still lead to ruin for an individual investor traveling through time, if it has a non-zero ruin probability. The ensemble average does not protect you.

Example: Russian Roulette with 5 empty chambers. Positive expected value across 6 players. Catastrophic for the one player on the losing path. Markets work the same way with leverage.

**Practical rule**: Never accept any strategy with a non-zero probability of total ruin, regardless of expected return. Size positions so that no single loss ends your ability to participate.

---

## Convexity and Optionality
A payoff is **convex** when gains from good scenarios exceed losses from bad scenarios of equal probability.

- Options (long) are convex: you lose the premium (small, bounded) or gain multiples (large, unbounded)
- Options (short) are concave: you gain the premium (small, bounded) or lose multiples (large, unbounded)
- Equity in companies with no debt and high optionality: convex
- Investment-grade corporate bonds: concave (small coupon upside, large default downside in tail)

Seek convexity. Avoid concavity. The "safe middle" is often the most dangerous because it appears low-risk while hiding negative convexity.

---

## Barbell Strategy
Avoid the middle of the risk distribution. Combine:
- **Very safe** (far left): assets with near-zero downside (cash, short-term government bonds, essential businesses with no debt)
- **Very speculative** (far right): assets with bounded downside and unbounded upside (deep options, early-stage ventures, distressed assets near zero)

**Avoid**: medium risk, medium return assets — investment-grade credit, "quality growth" stocks at high multiples. These *appear* safe but carry hidden negative convexity.

Portfolio construction: 85-90% very safe, 10-15% highly speculative with asymmetric upside. Never the dangerous middle at scale.

---

## Via Negativa
Improvement by subtraction, not addition. In medicine: first, do no harm. In investing: first, remove fragility.

- Don't add "hedges" — remove the exposure that requires hedging
- Don't add forecasting sophistication — remove dependence on forecasts
- Don't add complexity — remove the hidden leverage and correlation

The best risk management is not having the risk.

---

## Skin in the Game
Those who bear no downside from their decisions cannot be trusted.

- An investment banker fees regardless of outcome → noise
- A fund manager with assets in the fund, no hedges → signal
- Management selling shares while recommending → warning
- Management buying shares with own capital → meaningful signal

**Rule**: Weight advice in proportion to the advisor's personal exposure to being wrong.

---

## Fat Tails and the Fourth Quadrant
Normal distributions catastrophically underestimate tail probabilities in financial markets.

**Fourth Quadrant**: complex systems (financial markets) where both the probability of extreme events AND the magnitude of those events are unknowable. Standard statistical methods fail here.

Historical evidence:
- 2008 financial crisis: 25-standard-deviation event under Gaussian models (should happen once in the age of the universe)
- 1987 Black Monday: 22-standard-deviation event
- March 2020: volatility spikes that models said were near-impossible

**Practical implication**: Any risk model using normal distribution (VaR, Sharpe ratio) in financial markets is providing false confidence. Use these metrics to understand the *calm* regime only. They tell you nothing about the regime that matters most.

---

## Iatrogenics
Harm caused by the intervention itself. From medicine (doctor causes illness), but applies to investing.

- Over-hedging: the hedge introduces basis risk, counterparty risk, and complexity
- Over-diversification: diversification into correlated assets provides no protection when correlations converge to 1 in a crisis
- Frequent rebalancing: transaction costs, tax drag, and the illusion of control
- Risk models: using VaR makes institutions feel safe in ways that make the system more fragile

The intervention (risk management tool, hedge, model) can create the very fragility it's designed to prevent.
