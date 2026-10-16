# NFL PLAYER PROPS — FORMAL AUDIT & CALIBRATION REPORT
## League: NFL · Slate date: 2026-09-10 (Week 1 Thursday, SF @ LA, Melbourne) · Frozen run: `NFL-2026-W01-20260910T232547Z-THU_FINAL`

**Scope.** One league, one slate, one game. Dataset A frozen and unaltered. All grading is Dataset B. No real-money stake was authorized; the card is paper at 0u throughout.

**Purpose.** Answer the desk question — *did high-ranked model edge beat the close, price correctly, and outperform lower-ranked edge on this slate?* — and convert the answer into specific, testable changes to the Python pipeline, board by board.

**Verdict up front: NO on all three testable counts, and the close test is unrunnable.** Detail in Sections 2 and 3. Sample caveat in Section 6 — this is one game and nothing here is statistically significant. It is an instrument reading, not a verdict on the model.

---

# SECTION 1 — CLOSING-LINE SOURCING: RESULT AND EVIDENCE

The desk attempted to source closing prices independently rather than accept the capture package's DATA GAP at face value.

**Result: no verifiable close exists for any of the 46 propositions.** Every row stays `CLOSE_DATA_GAP`. What public archives preserve for this game is pre-kick *preview* pricing from 1–3 days before kickoff, at books and lines that differ from the frozen reference book, with no final pre-kick timestamp. Under the desk taxonomy that is `CLOSE_PROXY_PUBLIC_EARLY` at best, and it is not admissible as a close.

| Source | Date observed | What it preserves | Admissible as close? |
|---|---|---|---|
| BetMGM player-prop pages (Kyren Williams, Stafford, Nacua, Adams, Kittle breakdowns) | ~Sep 9–10, 2026 | Single-book prop lines, no price timestamp | No — early, single book, no timestamp |
| Football Nation prop research piece | Rechecked Sep 9, 1:00 p.m. Central | FanDuel / BetMGM / Fanatics lines with an explicit "lines can change" note | No — 34+ hours pre-kick |
| Bleacher Report TNF props update | Sep 10, 2026 | Mainline 48.5 total, LA −3.5, ML −210/+176 | No — mainline only, no timestamp |
| Sports Betting Dime Week 1 prop roundup | ~Sep 8, 2026 | Best-available lines across BetMGM / theScore / Caesars / bet365 | No — best-of-market composite |
| Action Network game page (via capture package) | Undated archive | Mainline spread/total/ML | No — no final timestamp |
| Odds archives with named-book timestamped prop scans | — | Not found for this game | N/A |

**What the public record does establish** (usable as market-width context, explicitly *not* as CLV):

| Proposition | Frozen handoff reference (Sep 10, 23:25Z) | Public pre-kick elsewhere | Read |
|---|---|---|---|
| Kyren Williams rushing yards | FanDuel 54.5 | BetMGM 55.5 | 1-yard cross-book spread |
| Kyren Williams rushing attempts | DraftKings 13.5 | BetMGM 12.5 | A full attempt of cross-book disagreement on the single-book market the model traded |
| Stafford passing yards | DraftKings 262.5 / FanDuel 258.5 | BetMGM 265.5, Fanatics 261.5 | 7-yard spread across four books |
| George Kittle receiving yards | DraftKings 33.5 | Reported drift 42.5 → 37 earlier in the week | Market moved hard against the model's OVER; Kittle finished with 12 |
| Puka Nacua receptions / receiving yards | 7.5 / 90.5 | 7.5 / 90.5 | Stable — the two most liquid props on the board |
| Game total | 47.5 | 48.5 at several books | 1-point spread |

**Consequence for this report.** The CLV test cannot be run. Sections 2 and 3 therefore score the model against the *pre-kick no-vig market price captured in the frozen snapshot itself*, which is the strongest admissible benchmark available. That is a weaker test than CLV — it measures whether the model priced better than the market it was quoted against, not whether it beat the market's final opinion — but it is a real test and the model can fail it, as it does.

---

# SECTION 2 — THE CASINO-QUANT SCORECARD

Scored set: **49 propositions** — every model-favored side with a two-sided quote, a gradeable player result, and no push. One row per player/market/line/side, best book. 13 distinct players, 7 stat families, one game.

| Test | Metric | Result | Verdict |
|---|---|---|---|
| **1. Did edge beat the close?** | CLV, price and probability delta | 0 of 46 closes recoverable | **UNGRADEABLE** — cannot be claimed either way |
| **2. Did the model price correctly?** | Brier vs market no-vig | Model p_raw **0.3126** vs market **0.2427** vs base rate **0.2499** | **FAIL** — worse than the market *and* worse than flipping a coin at the base rate |
| **3. Did high-ranked edge beat low-ranked edge?** | Spearman ρ, edge vs outcome | ρ = **-0.107** (p = 0.47) | **FAIL** — no rank ordering; sign is mildly negative |
| **4. Did EV rank predict ROI?** | Spearman ρ, conservative EV vs ROI | ρ = **-0.023** (p = 0.88) | **FAIL** — the EV ranking carried no information on this slate |
| **5. Was the quarantine filter right?** | ROI of blocked band | -6.56u on 22 props (−29.8%) | **PASS** — the block saved money |

## 2.1 Pricing accuracy against the market

| Forecaster | Brier | Log loss | Mean probability | Realized hit rate | Skill vs base rate |
|---|---:|---:|---:|---:|---:|
| Model `p_raw` | 0.3126 | 0.9145 | 0.693 | 0.490 | -25.1% |
| Model `p_conservative` | 0.2525 | 0.6983 | 0.564 | 0.490 | -1.0% |
| Market no-vig | 0.2427 | 0.6784 | 0.496 | 0.490 | +2.9% |
| Base rate (climatology) | 0.2499 | — | 0.490 | 0.490 | 0.0% |

The model claimed an average 69.3% on the sides it favored and hit 49.0%. That is **20.4 percentage points of overconfidence** on the raw layer. The uncertainty haircut does most of the work it was designed to do — `p_conservative` pulls the Brier from 0.3126 to 0.2525 — but it lands at the base rate, not past it. The market beat both layers.

This is the single most important number in the report. A pricing engine whose probabilities score worse than the price it is betting into has no demonstrated edge on this sample, regardless of the paper P&L.

## 2.2 Does more edge mean more money?

| Model-vs-market edge band | Props | Mean model P | Mean market P | Record | Hit rate | Net | ROI |
|---|---:|---:|---:|---|---:|---:|---:|
| 0–5pp | 5 | 0.541 | 0.514 | 2-3 | 40.0% | -1.46u | -29.2% |
| 5–10pp | 6 | 0.583 | 0.499 | 3-3 | 50.0% | -0.40u | -6.7% |
| 10–18.3pp | 14 | 0.649 | 0.506 | 10-4 | 71.4% | +4.38u | +31.3% |
| 18.3–30pp | 15 | 0.707 | 0.486 | 6-9 | 40.0% | -3.18u | -21.2% |
| 30pp+ | 9 | 0.897 | 0.485 | 3-6 | 33.3% | -3.28u | -36.4% |

**The relationship is inverted at the top.** The two widest bands — exactly where the model is most confident it has found something — produced the worst returns (−21% and −36%). The only profitable band is 10–18.3pp, which is where the actionable rows happen to sit. On 14 propositions that is as likely to be luck as signal, and the desk should not build a thesis on it.

## 2.3 Reliability curve

| Model probability bucket | Props | Mean model P | Realized | Calibration gap | Market said |
|---|---:|---:|---:|---:|---:|
| 50–60% | 9 | 55.2% | 55.6% | +0.3pp | 50.2% |
| 60–70% | 20 | 64.3% | 55.0% | -9.3pp | 49.4% |
| 70–80% | 12 | 73.9% | 41.7% | -32.2pp | 50.0% |
| 80–90% | 2 | 83.6% | 50.0% | -33.6pp | 48.3% |
| 90%+ | 6 | 93.4% | 33.3% | -60.1pp | 49.1% |

Monotonically worse as the model gets more confident. The 90%+ bucket — six propositions the model considered near-locks — hit 33%. Every one of those six is an RB carry or rushing-yard line whose volume assumption rested on backs who did not play.

## 2.4 Where the damage was

| Market | Props | Mean model P | Hit rate | Net |
|---|---:|---:|---:|---:|
| pass_attempts | 2 | 0.71 | 50% | -0.11u |
| pass_completions | 2 | 0.61 | 50% | -0.17u |
| pass_yds | 5 | 0.71 | 0% | -5.00u |
| reception_yds | 20 | 0.63 | 65% | +4.45u |
| receptions | 11 | 0.67 | 55% | +0.17u |
| rush_attempts | 3 | 0.95 | 67% | +0.84u |
| rush_yds | 6 | 0.82 | 17% | -4.12u |

Passing yards 0-for-5 and rushing yards 1-for-6 carried the losses. Reception yards was the only family with real positive return, and it is also the family where the model's dilution error happened to point the same way as the blowout.

---

# SECTION 3 — BOARD-BY-BOARD AUDIT AND CALIBRATION

Each board is scored on what it claimed, what happened, and what must change in the pipeline that produces it.

## Boards 1–3 — Full player forecast boards (market-blind)

| Measure | Value |
|---|---:|
| Series published | 70 |
| Series gradeable | 38 (54%) |
| Series VOID (player never on gamebook active list) | 32 (46%) |
| P10–P90 coverage (nominal 80%) | 76.3% |
| Mean bias (actual − model mean) | -5.97 |
| MAE | 16.09 |
| Direction at model-native lines | 21-17 |

**Defect 1 — the board is 46% fiction.** Thirty-two series belonged to players who never appeared on an active list. Ricky Pearsall was publicly reported out for the season on August 21, three weeks before this run, and the simulator still allocated him 3.0 targets at role certainty 79.

**Defect 2 — the reference-line method manufactures a fake UNDER lean.** MODEL_NATIVE lines are set at the half-point nearest the *mean*, and on right-skewed count distributions the median sits below the mean, so the board tilts UNDER by construction. That lean is a property of the line-setter, not a football read, and it should never have been presented in a column called "Model Pick".

**Defect 3 — intervals are too narrow where it matters.** All three Stafford series finished outside their own P10–P90. Corum and Kaelon Black finished above P90 on both carries and yards. Coverage looks fine in aggregate (76%) and is structurally broken in the RB and QB-volume families.

**Patches.** B1-P1: exclude any series whose player is not on a verified active list before the board is written; publish an explicit `EXCLUDED_NOT_ACTIVE` register instead of silently carrying them. B1-P2: set MODEL_NATIVE reference lines at the **median**, or drop the pick column and publish distribution only. B1-P3: widen or fatten the tails on QB volume and RB carries until backtested coverage reaches nominal.

## Board 4 — Most-probable-direction board

The top of this board was dominated by extreme-disagreement rows: Corum rush attempts UNDER at 0.992, Kyren at 0.948, McCaffrey at 0.905. Those three, as a set, went 2-1 but the 0.992 lost outright — Corum ran 10 times against a 9.5 line.

**Defect.** A probability board sorted by raw probability surfaces the model's worst-calibrated rows first, because extreme probabilities come from extreme role assumptions. **Patch B4-P1:** sort by calibrated probability and suppress any row whose upstream volume market is quarantined; annotate each row with its own market's quarantine status.

## Boards 5–7 — Market-lined pick boards

| Model probability bucket | Rows | Mean model P | Record | Hit rate | Calibration gap |
|---|---:|---:|---|---:|---:|
| 50–60% | 6 | 55.4% | 3-3 | 50% | -5.4pp |
| 60–70% | 14 | 64.0% | 8-6 | 57% | -6.9pp |
| 70–80% | 8 | 74.8% | 4-4 | 50% | -24.8pp |
| 80%+ | 6 | 90.6% | 3-3 | 50% | -40.6pp |
| **All** | 34 | 69.7% | 18-16 | 53% | -16.8pp |

Overall 18-16 at a mean claimed probability of 69.7% — a 16.8-point calibration miss on the board the desk uses to judge directional skill. **Patch B5-P1:** publish this calibration table automatically with every run and fail the board if the top bucket underperforms the bottom bucket. **Patch B5-P2:** carry each row's book count; the single-book rows (pass attempts, rush attempts) are priced off one no-vig anchor and should be labelled low-trust in the board itself, not only in the risk room.

## Board 8 — EV+ board

| Accounting basis | Rows | Record | Net | ROI |
|---|---:|---|---:|---:|
| All EV rows, flat 1u | 12 | 7-5-0 | +1.123u | +9.36% |
| Unique propositions, best price | 9 | 6-3-0 | +2.474u | +27.49% |
| Scored against market (two-sided only) | 7 | 5-2-0 | +2.43u | +34.8% |

**The P&L is real and the process signal is absent.** Section 2 shows EV rank had no correlation with ROI. The card won because LA got blown out, not because the EV ordering identified anything.

**Defect 1 — one-sided quotes reach ACTIONABLE.** Stafford completions OVER 22.5 printed +11.77% at BetRivers purely because a one-sided quote skipped the market blend; the two-sided DraftKings version of the identical proposition was rejected at +0.97%. It lost. **Patch B8-P1: block one-sided quotes from ACTIONABLE entirely.** If no two-sided anchor exists at that line, the row is PAPER_ONLY at most, and it inherits the two-sided row's BUY-TO and HARD STOP when one exists at the same line.

**Defect 2 — BUY-TO can sit worse than the reference price.** Stribling receptions UNDER 2.5 shipped ACTIONABLE at +110 with a BUY-TO of +111. A row that is out of price at its own reference price should never be published as actionable. **Patch B8-P2:** assert `reference_price ≥ buy_to_price` at write time; fail the row otherwise.

**Defect 3 — duplicate expressions inflate the headline.** Twelve rows are nine propositions and four theses. **Patch B8-P3:** publish ROI and counts at all three levels and headline the thesis level.

## Board 9 — Edge leaderboard

Ranking power measured: Spearman ρ between conservative EV and realized ROI = **-0.023** (p = 0.88); between raw edge and outcome = **-0.107** (p = 0.47). The leaderboard ordered nothing.

**Patch B9-P1:** add a persistent rank-integrity metric to every postgame run — Spearman ρ of edge rank versus outcome, plus decile ROI — and track it across slates. A leaderboard that cannot demonstrate rank ordering over a rolling window is a presentation artifact, not a signal.

## Board 10 — Rejection board

| Rejected set | Props | Record | Net | ROI |
|---|---:|---|---:|---:|
| EXTREME_MODEL_MARKET_DISAGREEMENT | 22 | 8-14 | -6.56u | −29.8% |
| INSUFFICIENT_EV (model-favored side) | 20 | 11-9 | +0.18u | +0.9% |

**This board earned its keep and is the best-performing component in the packet.** The extreme filter blocked a band that lost at −30%, and it got worse the wider the gap. **Patch B10-P1:** keep the 18.3pp cutoff, but log every blocked proposition's outcome permanently so the threshold can be tuned on evidence rather than intuition. **Patch B10-P2:** when a proposition is quarantined, automatically quarantine or demote its downstream derivatives at the same player — the packet let McCaffrey rushing yards through while his rush attempts were blocked at 40.4pp, and the yards row lost.

## Board 11 — Market availability and data quality

Reported 77/77 provider checks OK while the role tree contained twelve non-participants, one of them publicly ruled out for the season three weeks earlier. The health check measured provider reachability, not data correctness.

**Patch B11-P1:** add content assertions to provider health — active-roster coverage rate, share of modeled volume on unconfirmed players, and stale-prior detection (`games_observed = 0` bootstrap on a market-posted starter). Fail the run if modeled volume on unconfirmed players exceeds a set threshold. On this slate the figure was 30–43% and the run shipped clean.

## Board 12 — Correlation and thesis map

The thesis collapse worked: Python named Kyren receptions UNDER the best expression of RECEIVER_ROLE_DOWN and flagged Nacua, Corum and Stribling redundant. Outcomes: Kyren lost, the three "redundant" rows went 3-0. **The collapse selected the worst expression of its own thesis.**

**Patch B12-P1:** rank expressions within a thesis by role certainty and market liquidity, not by conservative EV alone. The redundant rows that won were the ones on higher-liquidity, better-understood markets.

## Board 13 — Game desk

Called the game environment pass-heavy for both teams: LA 41.7 pass plays, SF 38.8. Actual: LA 28 attempts, SF 34. The model was close on SF and 13.7 plays wrong on LA. **Patch B13-P1:** publish a game-script sensitivity band — what the player board looks like at the 20th and 80th percentile of team pass volume — so a single point estimate of team volume cannot silently drive the whole card.

## Board 14 — Final action list and desk overlay

| Desk gate | Rows | Record | Net | ROI |
|---|---:|---|---:|---:|
| VALUE | 5 | 3-2 | +0.213u | +4.27% |
| WATCH | 7 | 4-3 | +0.910u | +13.00% |

The overlay demoted the right rows for the right reasons and still underperformed on P&L over 12 rows. Keep the flags, do not tune them on one slate, and log gate-level ROI every week.

---

# SECTION 4 — PIPELINE CHANGE SPECIFICATION

Ordered by expected impact. Each is testable and each has slate evidence.

| ID | Change | Where | Acceptance test | Evidence |
|---:|---|---|---|---|
| **P1** | Active-roster gate before simulation. Any player not on a verified active list is removed from the role tree and their volume redistributed across confirmed players. Publish the exclusion register. | Role-state build, pre-simulation | No published series belongs to a non-participant; exclusion register non-empty and correct on a replay of this slate | 32/70 series VOID; Pearsall modeled at 3.0 targets after being reported out for the season on Aug 21 |
| **P2** | Volume-mass reconciliation after the gate. Team target mass and carry mass must tie to confirmed active players within tolerance, or the run fails. | Post-simulation validation | Run aborts when >15% of modeled volume sits on unconfirmed players | 30–43% of every modeled volume pool was on non-participants |
| **P3** | Two-sided quote requirement for ACTIONABLE. One-sided quotes may inform but never price. | EV engine | No ACTIONABLE row lacks `market_novig_prob` | Stafford completions +11.77% one-sided vs +0.97% two-sided, lost |
| **P4** | Price-guard assertion: reference price must be at least as good as BUY-TO. | EV engine write step | Assertion failure on the Stribling row in a replay | Stribling shipped ACTIONABLE at +110 with BUY-TO +111 |
| **P5** | Automated pre-kick close capture: book, line, price, timestamp for every board candidate, stored to Dataset B. | New scheduled job, T-10 to T-0 minutes | ≥90% of candidates carry a `CLOSE_EXACT_SAME_BOOK` record | 0 of 46 closes recoverable after the fact; CLV untestable |
| **P6** | Calibration layer on model probabilities, fitted on accumulated Dataset B, replacing the identity-shrinkage placeholder. | Probability layer | Rolling Brier beats market no-vig on held-out slates before any row may grade above VALUE | Model Brier 0.3126 vs market 0.2427 vs base rate 0.2499 |
| **P7** | Downstream quarantine propagation: quarantining a volume market quarantines or demotes its yardage derivative for the same player. | Gate engine | McCaffrey rushing yards demoted in a replay of this slate | Rush attempts blocked at 40.4pp; rushing yards shipped ACTIONABLE and lost |
| **P8** | MODEL_NATIVE reference lines at the median, not the mean; or remove the pick column from market-blind boards. | Forecast board writer | UNDER share of model-native picks within 45–55% on replay | Structural UNDER tilt on right-skewed counts |
| **P9** | Interval widening on QB volume and RB carries until backtested P10–P90 coverage reaches nominal. | Distribution layer | Coverage 78–82% on a rolling window | 3 below P10, 6 above P90; all Stafford series outside band |
| **P10** | Rank-integrity metric published every postgame: Spearman ρ of edge rank vs outcome, decile ROI, gate-level ROI. | Postgame audit job | Metric present in every recap; rolling window tracked | ρ = −0.107 edge vs outcome, −0.023 EV vs ROI |
| **P11** | Three-level ROI reporting — per row, per proposition, per thesis — with the thesis level as the headline. | Recap writer | Headline number is thesis-level in every recap | 12 rows = 9 props = 4 theses; +9.36% vs +27.49% on identical outcomes |
| **P12** | Provider health becomes content-aware: active-roster coverage, bootstrap-prior-on-starter detection, stale-history detection. | Provider health module | Run flags Evans/Deebo/Stribling bootstrap and Henderson/Freeman stale history on replay | 77/77 checks OK on a slate with a broken role tree |

---

# SECTION 5 — WHAT TO PERSIST FOR CALIBRATION

Dataset B must carry these fields per proposition, every slate, or the questions in Section 2 stay unanswerable:

```text
run_id, candidate_id, forecast_id, player, market, side, line
p_raw, p_calibrated, p_blend, p_conservative, market_novig_prob
edge_pp, ev_conservative_pct, ev_rank, confidence, role_certainty
reference_book, reference_odds, reference_timestamp
close_book, close_line, close_odds, close_timestamp, close_quality_flag   <-- currently always DATA GAP
clv_price_delta, clv_probability_delta, clv_positive_flag                 <-- blocked until P5 ships
participation_status, actual, y_outcome, push_flag, roi_per_1u
brier_contribution, logloss_contribution, edge_bucket, prob_bucket
thesis_id, expression_rank_within_thesis, desk_gate
```

Minimum sample before any calibration conclusion is acted on: **200 scored propositions across at least 20 games**, with no more than 15% from any single game. This slate contributes 49 propositions from 13 players in 1 game; its effective independent sample is closer to 8.

---

# SECTION 6 — SAMPLE-SIZE HONESTY

Everything in Section 2 is one game. The p-values on the rank tests are 0.47 and 0.88 — the correct statistical reading is "no detectable relationship", not "an inverse relationship". The Brier comparison is the most robust of the findings because it aggregates 49 probability statements, but even that is dominated by one game script and by correlated within-game outcomes.

What would change the verdict:

- Model Brier beating market no-vig over a rolling 200-proposition window → the pricing failure was slate-specific.
- Positive, stable Spearman ρ on edge rank over the same window → the leaderboard has ordering power.
- Any CLV evidence at all once P5 ships → the primary test becomes runnable.

What does **not** need more data, because it is a data-integrity defect rather than a statistical one: the role tree containing twelve non-participants, the one-sided quote reaching ACTIONABLE, and the BUY-TO inversion. Those are bugs, and they should be fixed before the next slate regardless of what any future sample says.

---

# APPENDIX A — THE 49 SCORED PROPOSITIONS

| # | Player | Market | Side | Line | Book | Price | Model P | Market P | Edge | Actual | Result | ROI | Status |
|---:|---|---|---|---:|---|---:|---:|---:|---:|---:|---|---:|---|
| 1 | Blake Corum | rush_attempts | UNDER | 9.5 | DraftKings | +103 | 0.992 | 0.465 | +52.7pp | 10 | LOSS | -1.000 | EXTREME |
| 2 | Christian McCaffrey | rush_attempts | UNDER | 15.5 | DraftKings | +101 | 0.905 | 0.469 | +43.6pp | 10 | WIN | +1.010 | EXTREME |
| 3 | Blake Corum | rush_yds | UNDER | 43.5 | BetRivers | -112 | 0.927 | 0.492 | +43.5pp | 54 | LOSS | -1.000 | EXTREME |
| 4 | Kyren Williams | rush_attempts | UNDER | 13.5 | DraftKings | -121 | 0.948 | 0.517 | +43.2pp | 11 | WIN | +0.826 | EXTREME |
| 5 | Blake Corum | rush_yds | UNDER | 42.5 | FanDuel | -113 | 0.920 | 0.500 | +42.0pp | 54 | LOSS | -1.000 | EXTREME |
| 6 | Blake Corum | rush_yds | UNDER | 41.5 | DraftKings | -113 | 0.912 | 0.502 | +41.0pp | 54 | LOSS | -1.000 | EXTREME |
| 7 | Mike Evans | reception_yds | UNDER | 49.5 | DraftKings | -113 | 0.859 | 0.502 | +35.7pp | 49 | WIN | +0.885 | EXTREME |
| 8 | Mike Evans | receptions | UNDER | 3.5 | DraftKings | +103 | 0.814 | 0.464 | +34.9pp | 6 | LOSS | -1.000 | EXTREME |
| 9 | Christian McCaffrey | receptions | UNDER | 4.5 | DraftKings | +108 | 0.796 | 0.453 | +34.2pp | 5 | LOSS | -1.000 | EXTREME |
| 10 | Matthew Stafford | pass_attempts | OVER | 34.5 | DraftKings | -101 | 0.763 | 0.473 | +29.0pp | 25 | LOSS | -1.000 | EXTREME |
| 11 | Kyren Williams | rush_yds | UNDER | 54.5 | DraftKings | -114 | 0.765 | 0.504 | +26.1pp | 41 | WIN | +0.877 | EXTREME |
| 12 | Davante Adams | receptions | UNDER | 4.5 | DraftKings | -113 | 0.749 | 0.500 | +24.9pp | 3 | WIN | +0.885 | EXTREME |
| 13 | Christian McCaffrey | reception_yds | UNDER | 40.5 | BetRivers | -117 | 0.750 | 0.503 | +24.7pp | 20 | WIN | +0.855 | EXTREME |
| 14 | Christian McCaffrey | reception_yds | UNDER | 39.5 | DraftKings | -113 | 0.739 | 0.502 | +23.7pp | 20 | WIN | +0.885 | EXTREME |
| 15 | Brock Purdy | pass_yds | OVER | 236.5 | DraftKings | -112 | 0.720 | 0.500 | +22.0pp | 205 | LOSS | -1.000 | EXTREME |
| 16 | Matthew Stafford | pass_yds | OVER | 258.5 | FanDuel | -113 | 0.720 | 0.500 | +22.0pp | 155 | LOSS | -1.000 | EXTREME |
| 17 | Brock Purdy | pass_yds | OVER | 238.5 | FanDuel | -113 | 0.712 | 0.500 | +21.2pp | 205 | LOSS | -1.000 | EXTREME |
| 18 | Blake Corum | receptions | UNDER | 0.5 | DraftKings | +122 | 0.631 | 0.425 | +20.6pp | 0 | WIN | +1.220 | EXTREME |
| 19 | Matthew Stafford | pass_yds | OVER | 262.5 | DraftKings | -111 | 0.704 | 0.499 | +20.5pp | 155 | LOSS | -1.000 | EXTREME |
| 20 | Christian McCaffrey | rush_yds | UNDER | 59.5 | DraftKings | -110 | 0.700 | 0.496 | +20.4pp | 68 | LOSS | -1.000 | EXTREME |
| 21 | Brock Purdy | pass_yds | OVER | 240.5 | BetRivers | -115 | 0.703 | 0.500 | +20.3pp | 205 | LOSS | -1.000 | EXTREME |
| 22 | Deebo Samuel Sr. | receptions | UNDER | 2.5 | DraftKings | +114 | 0.635 | 0.441 | +19.3pp | 6 | LOSS | -1.000 | EXTREME |
| 23 | Christian McCaffrey | rush_yds | UNDER | 58.5 | FanDuel | -113 | 0.687 | 0.500 | +18.7pp | 68 | LOSS | -1.000 | ACTIONABLE |
| 24 | De'Zhaun Stribling | receptions | UNDER | 2.5 | DraftKings | +110 | 0.634 | 0.449 | +18.5pp | 0 | WIN | +1.100 | ACTIONABLE |
| 25 | Davante Adams | reception_yds | UNDER | 53.5 | FanDuel | -113 | 0.682 | 0.500 | +18.2pp | 26 | WIN | +0.885 | ACTIONABLE |
| 26 | Puka Nacua | receptions | UNDER | 7.5 | DraftKings | -149 | 0.743 | 0.565 | +17.8pp | 5 | WIN | +0.671 | ACTIONABLE |
| 27 | Davante Adams | reception_yds | UNDER | 52.5 | DraftKings | -113 | 0.672 | 0.502 | +17.0pp | 26 | WIN | +0.885 | ACTIONABLE |
| 28 | Kyren Williams | receptions | UNDER | 1.5 | DraftKings | +114 | 0.602 | 0.441 | +16.1pp | 3 | LOSS | -1.000 | ACTIONABLE |
| 29 | Brock Purdy | pass_attempts | OVER | 33.5 | DraftKings | -112 | 0.659 | 0.499 | +16.0pp | 34 | WIN | +0.893 | ACTIONABLE |
| 30 | Davante Adams | reception_yds | UNDER | 51.5 | BetRivers | -117 | 0.662 | 0.503 | +15.9pp | 26 | WIN | +0.855 | REJECTED |
| 31 | Deebo Samuel Sr. | reception_yds | UNDER | 29.5 | BetRivers | -117 | 0.644 | 0.503 | +14.1pp | 48 | LOSS | -1.000 | REJECTED |
| 32 | De'Zhaun Stribling | reception_yds | UNDER | 29.5 | DraftKings | -114 | 0.644 | 0.504 | +13.9pp | 0 | WIN | +0.877 | REJECTED |
| 33 | Deebo Samuel Sr. | reception_yds | UNDER | 28.5 | FanDuel | -113 | 0.628 | 0.500 | +12.8pp | 48 | LOSS | -1.000 | REJECTED |
| 34 | Blake Corum | reception_yds | UNDER | 2.5 | DraftKings | -115 | 0.634 | 0.506 | +12.7pp | 0 | WIN | +0.870 | REJECTED |
| 35 | Puka Nacua | reception_yds | UNDER | 90.5 | DraftKings | -113 | 0.623 | 0.502 | +12.1pp | 74 | WIN | +0.885 | REJECTED |
| 36 | George Kittle | receptions | UNDER | 3.5 | DraftKings | -148 | 0.680 | 0.563 | +11.6pp | 2 | WIN | +0.676 | REJECTED |
| 37 | Deebo Samuel Sr. | reception_yds | UNDER | 27.5 | DraftKings | -111 | 0.611 | 0.498 | +11.3pp | 48 | LOSS | -1.000 | REJECTED |
| 38 | De'Zhaun Stribling | reception_yds | UNDER | 27.5 | FanDuel | -113 | 0.611 | 0.500 | +11.1pp | 0 | WIN | +0.885 | REJECTED |
| 39 | Puka Nacua | reception_yds | UNDER | 86.5 | BetRivers | -114 | 0.593 | 0.497 | +9.6pp | 74 | WIN | +0.877 | REJECTED |
| 40 | Matthew Stafford | pass_completions | OVER | 22.5 | DraftKings | -131 | 0.630 | 0.535 | +9.5pp | 15 | LOSS | -1.000 | REJECTED |
| 41 | Kyren Williams | reception_yds | UNDER | 10.5 | DraftKings | -118 | 0.603 | 0.512 | +9.1pp | 24 | LOSS | -1.000 | REJECTED |
| 42 | Tyler Higbee | receptions | UNDER | 1.5 | DraftKings | +116 | 0.523 | 0.437 | +8.7pp | 2 | LOSS | -1.000 | REJECTED |
| 43 | Brock Purdy | pass_completions | OVER | 21.5 | DraftKings | -120 | 0.592 | 0.515 | +7.7pp | 25 | WIN | +0.833 | REJECTED |
| 44 | Tyler Higbee | reception_yds | UNDER | 16.5 | FanDuel | -113 | 0.558 | 0.500 | +5.8pp | 12 | WIN | +0.885 | REJECTED |
| 45 | Colby Parkinson | reception_yds | OVER | 18.5 | DraftKings | -111 | 0.546 | 0.498 | +4.9pp | 6 | LOSS | -1.000 | REJECTED |
| 46 | Tyler Higbee | reception_yds | UNDER | 15.5 | DraftKings | -108 | 0.534 | 0.492 | +4.3pp | 12 | WIN | +0.926 | REJECTED |
| 47 | George Kittle | reception_yds | OVER | 32.5 | BetRivers | -115 | 0.520 | 0.500 | +2.0pp | 12 | LOSS | -1.000 | REJECTED |
| 48 | Colby Parkinson | receptions | UNDER | 2.5 | DraftKings | -163 | 0.598 | 0.585 | +1.4pp | 1 | WIN | +0.613 | REJECTED |
| 49 | George Kittle | reception_yds | OVER | 33.5 | DraftKings | -109 | 0.505 | 0.494 | +1.2pp | 12 | LOSS | -1.000 | REJECTED |

# APPENDIX B — PER-PLAYER CONTRIBUTION

| Player | Props | Mean model P | Record | Net |
|---|---:|---:|---|---:|
| Deebo Samuel Sr. | 4 | 0.63 | 0-4 | -4.00u |
| Matthew Stafford | 4 | 0.70 | 0-4 | -4.00u |
| Blake Corum | 6 | 0.84 | 2-4 | -1.91u |
| George Kittle | 3 | 0.57 | 1-2 | -1.32u |
| Brock Purdy | 5 | 0.68 | 2-3 | -1.27u |
| Colby Parkinson | 2 | 0.57 | 1-1 | -0.39u |
| Kyren Williams | 4 | 0.73 | 2-2 | -0.30u |
| Christian McCaffrey | 6 | 0.76 | 3-3 | -0.25u |
| Mike Evans | 2 | 0.84 | 1-1 | -0.12u |
| Tyler Higbee | 3 | 0.54 | 2-1 | +0.81u |
| Puka Nacua | 3 | 0.65 | 3-0 | +2.43u |
| De'Zhaun Stribling | 3 | 0.63 | 3-0 | +2.86u |
| Davante Adams | 4 | 0.69 | 4-0 | +3.51u |

Four players account for the entire result. Adams, Nacua and Stribling went 10-0 on volume that collapsed in a blowout; Stafford and Deebo went 0-8. None of that is skill on this sample.

---

```text
============================================================
NFL 2026-09-10 SF @ LA — AUDIT & CALIBRATION SUMMARY
============================================================
CLV TEST:            UNGRADEABLE (0/46 closes recoverable)
PRICING TEST:        FAIL (model Brier 0.3126 vs market 0.2427 vs base 0.2499)
RANK TEST:           FAIL (Spearman edge vs outcome -0.107, p=0.47)
EV RANK vs ROI:      FAIL (Spearman -0.023, p=0.88)
QUARANTINE FILTER:   PASS (blocked band -29.8%)
OVERCONFIDENCE:      +20.3pp on the raw probability layer
ROOT DEFECT:         30-43% of modeled volume on non-participants
PAPER P&L:           +9.36% per row / +27.49% per proposition (not evidence)
PRIORITY FIXES:      P1 roster gate, P3 two-sided requirement, P5 close capture
REAL-MONEY STATUS:   BLOCKED
============================================================
```