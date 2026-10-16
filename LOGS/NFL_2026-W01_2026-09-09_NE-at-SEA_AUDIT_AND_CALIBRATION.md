# NFL — FORMAL AUDIT & CALIBRATION REPORT
## League: NFL · Season 2026 · Week 01 · Slate Date 2026-09-09 · NE @ SEA

| Field | Value |
|---|---|
| League | NFL |
| Slate | 2026 Week 01 |
| Slate date (local kickoff) | 2026-09-09, 8:20 PM ET |
| Kickoff (UTC) | 2026-09-10T00:20Z |
| Game | New England Patriots @ Seattle Seahawks |
| Venue | Lumen Field, Seattle |
| AITA event ID | `NFL-EVT-375BDA7E7839E10C` |
| ESPN event ID | `401872656` |
| Controlling run | `NFL-2026-W01-20260909T210629Z-WED_INACTIVES` |
| Archived run | `NFL-2026-W01-20260909T130956Z-WED_NOW` |
| Model version | 0.3.0a4 · 500,000 draws · seed 260901 |
| Config hash | `79c45da9e087dc0ff4cbe81742e89c2aaec7161b5528eddc78819651520ca6c1` |
| Git commit | `b4738dd8779a674f0d0074c65172e02614aff9c4` |
| Final score | Seattle 13, New England 10 (no OT) |
| Capital deployed | **0u. No real-money authorization. All P&L hypothetical at reference prices, flat 1u.** |
| Audit status | `DATASET_B_SEED_SLATE` — n=1, no walk-forward artifact exists yet |

---

# PART I — THE CASINO-QUANT SCORE

> **The question:** did high-ranked model edge consistently beat the close, price correctly, and outperform lower-ranked edge across this slate?

## Verdict summary

| Test | Result | Grade |
|---|---|---|
| **1. Beat the close** | 3 comparable rows, all negative. No true closes exist. | **UNPROVEN — leaning FAIL** |
| **2. Price correctly** | Better than market on probability scoring, worse than market on point estimates. Conservative layer is under-confident by 9.3pp. | **PARTIAL PASS** |
| **3. High rank beats low rank** | Spearman ρ = −0.05. Top EV quintile +17% ROI; bottom quintile +60%. Top 3 by EV lost money. | **FAIL** |

**Composite score: the model produced money on this slate and its ranking did not explain where the money came from.** Positive return with zero rank discrimination is indistinguishable from a lucky draw across a broadly mispriced board. That is the honest reading at n=1.

---

## TEST 1 — Did high-ranked edge beat the close?

### Closing-line sourcing: attempted and documented

Public closing lines for individual player props are not archived in any accessible source. A sourcing attempt was made across sportsbook editorial, aggregator and preview coverage for this game. What exists publicly is **pre-kickoff editorial line reporting**, not timestamped closes.

What was recoverable, and its use:

| Source date | Recoverable fact | Audit use |
|---|---|---|
| 2026-09-08 | Stevenson's widely posted rushing-yards threshold climbed from 41.5 to 55.5 | Confirms sustained upward market pressure on Stevenson volume; our T-3h snapshot had 57.5/59.5 |
| 2026-09-08 | Stevenson rush attempts 15.5 characterised in market commentary as the market overreacting to an injury report | Independent confirmation the 15.5 line was contested, not stale |
| 2026-09-09 | Maye passing yards 232.5 at −113 (DraftKings); 226.5 at −115 (bet365); pass attempts 32.5 and completions 20.5 (BetMGM) | Our reference prices sit inside the public market range — no evidence we were quoting an off-market book |
| 2026-09-08 | Forecast 76°F, wind 5 mph, no weather angle | **Closes the weather DATA GAP carried through both pre-kickoff board renders** |
| 2026-09-08 | TreVeyon Henderson (ankle) did not practice Monday | Explains the Henderson inactive; the handoff had no injury artifact |

None of this qualifies as `TRUE_CLOSE`. The audit therefore records:

```
TRUE_CLOSE rows:        0
CLOSE_PROXY_CONSENSUS:  10
NO_CLOSE_CAPTURED:      197
```

### The three comparable rows

Same line at entry and close, so CLV is computable:

| Proposition | Reference | Implied | Close proxy | Implied | Δ |
|---|---:|---:|---:|---:|---:|
| Kupp UNDER 2.5 receptions | +100 | 50.00% | +108 | 48.08% | **−1.92pp** |
| Henry UNDER 3.5 receptions | −200 | 66.67% | −164 | 62.12% | **−4.55pp** |
| Maye OVER 32.5 pass attempts | −109 | 52.15% | −103 | 50.74% | **−1.41pp** |

**0 for 3. Mean CLV −2.63pp.**

Four further Tier-1 rows saw the line itself move (pass yards 230.5/232.5 → 231.5; completions 20.5 → 19.5) and are structurally incomparable — a changed line is a changed proposition.

### Verdict

**UNPROVEN, leaning FAIL.** Three negative comparables against consensus proxies is not a verdict, but it is not encouraging either. The direction is consistent: on every row where a like-for-like comparison exists, the market drifted away from our side after we priced it.

This is the single largest measurement failure in the package. **A desk that cannot measure CLV cannot know whether it has an edge.** Everything else in this report is secondary to fixing it.

---

## TEST 2 — Did the model price correctly?

Sample: 54 graded model-side rows (positive conservative EV), 34 unique propositions.

### Probability calibration — `p_conservative` buckets

| Predicted bucket | n | Mean predicted | Realized | Gap | Units | ROI |
|---|---:|---:|---:|---:|---:|---:|
| 0.45–0.55 | 10 | 52.3% | **100.0%** | +47.7pp | +10.69 | +106.9% |
| 0.55–0.60 | 23 | 57.9% | 60.9% | +2.9pp | +3.12 | +13.6% |
| 0.60–0.65 | 14 | 62.1% | 71.4% | +9.4pp | +4.30 | +30.7% |
| 0.65–0.70 | 6 | 67.4% | **33.3%** | **−34.1pp** | −2.66 | −44.3% |
| 0.70+ | 1 | 70.3% | 100.0% | +29.7pp | +0.50 | +50.0% |

**The calibration curve is non-monotonic and inverted at the top.** The bucket the model was least sure about went 10-0. The bucket it was most sure about (0.65–0.70) went 2-4.

### Layer comparison

| Layer | Mean predicted | Realized | Bias | Brier | Log loss |
|---|---:|---:|---:|---:|---:|
| `p_raw` | 78.0% | 68.5% | **−9.5pp (over-confident)** | 0.2365 | 0.7058 |
| `p_conservative` | 59.2% | 68.5% | **+9.3pp (under-confident)** | **0.2365** | **0.6666** |
| Market no-vig | — | 68.5% | — | 0.2528 | 0.6990 |

Two findings of substance:

1. **The conservative shrinkage overshot.** `p_raw` was over-confident by 9.5pp; `p_conservative` is under-confident by 9.3pp. The haircut did not calibrate the model, it flipped the sign of the error and kept roughly the same magnitude. It is currently a blunt instrument, not a calibrator.

2. **On probability scoring, the model narrowly beat the market.** Brier 0.2365 against 0.2528; log loss 0.6666 against 0.6990. On the subset where the model claimed an edge, its probabilities were better-ordered than the book's no-vig line. That is the one genuinely encouraging result in this report.

### Point-estimate accuracy — head to head against the posted line

25 player/market pairs where the model had a mean and the market had a line:

| | Model MAE | Market MAE | Model wins |
|---|---:|---:|---:|
| **All pairs (n=25)** | **13.98** | **12.14** | 12 / 25 |
| High role certainty ≥85 (n=17) | 16.53 | 12.68 | 7 / 17 |
| Low role certainty <85 (n=8) | **8.57** | 11.00 | 5 / 8 |

**The model is less accurate where it is most confident.** On the players it rated 87–94 role certainty it lost the accuracy contest 7–17 and posted a 30% higher MAE than the market. On the bootstrap players it rated 53 it beat the market outright.

Worst individual misses, all high certainty:

| Player | Stat | Model | Market | Actual | Model err | Market err |
|---|---|---:|---:|---:|---:|---:|
| Drake Maye | pass yards | 278.64 | 230.5 | 178 | **100.6** | 52.5 |
| Jaxon Smith-Njigba | rec yards | 52.47 | 81.5 | 122 | **69.5** | 40.5 |
| Rhamondre Stevenson | rec yards | 16.46 | 23.5 | 44 | **27.5** | 20.5 |
| Rhamondre Stevenson | rush attempts | 9.12 | 15.5 | 18 | **8.9** | 2.5 |

Best individual wins, mostly low certainty:

| Player | Stat | Model | Market | Actual | Model err | Market err |
|---|---|---:|---:|---:|---:|---:|
| A.J. Brown | rec yards | 29.30 | 64.5 | 26 | **3.3** | 38.5 |
| Mack Hollins | rec yards | 34.17 | 9.5 | 51 | **16.8** | 41.5 |
| Romeo Doubs | rec yards | 29.28 | 35.5 | 0 | **29.3** | 35.5 |
| Rashid Shaheed | rec yards | 22.00 | 31.5 | 4 | **18.0** | 27.5 |

### Verdict

**PARTIAL PASS.** The probability layer is better-ordered than the market. The point-estimate layer is not. And `role_certainty_score` — the field the desk uses to size confidence — is **inversely related to accuracy on this slate**.

---

## TEST 3 — Did high-ranked edge outperform low-ranked edge?

This is the test that matters most for a desk, because it determines whether the board's sort order is worth anything.

### EV quintiles — unique propositions, best price (n=34)

| Quintile | n | Mean EV | Hit rate | Units | ROI |
|---|---:|---:|---:|---:|---:|
| **Q1 (top)** | 7 | 20.3% | 57.1% | +1.19 | **+17.1%** |
| Q2 | 7 | 13.8% | 57.1% | +0.85 | +12.1% |
| Q3 | 6 | 10.6% | 100.0% | +5.10 | +85.0% |
| Q4 | 7 | 7.4% | 57.1% | +0.18 | +2.5% |
| **Q5 (bottom)** | 7 | 3.2% | 85.7% | +4.19 | **+59.9%** |

### Rank correlation

```
Spearman ρ (EV, unit P/L) = -0.050   p = 0.777
Spearman ρ (EV, hit)      = -0.171   p = 0.333
```

**Zero rank discrimination, with a mild inversion.** Conservative EV percentage carried no information about which propositions would win.

### Top-N cumulative curve

| Top N by EV | EV floor | W–L | Units | ROI |
|---|---:|---|---:|---:|
| Top 3 | 20.21% | 1–2 | **−0.380** | **−12.7%** |
| Top 5 | 17.55% | 3–2 | +1.375 | +27.5% |
| Top 8 | 16.21% | 5–3 | +2.079 | +26.0% |
| Top 10 | 14.92% | 6–4 | +2.005 | +20.1% |
| Top 15 | 11.54% | 9–6 | +2.927 | +19.5% |
| Top 20 | 9.85% | 14–6 | +7.141 | +35.7% |
| Top 26 | 5.45% | 18–8 | +8.318 | +32.0% |

A correctly ranked board produces a **downward-sloping** cumulative ROI curve — best at the top, decaying as you go deeper. This curve slopes the wrong way. The three highest-EV propositions on the entire board lost money; returns improved as the board got worse.

### Secondary ranking fields — also non-discriminating

**Confidence score:**

| Bucket | n | Hit | ROI |
|---|---:|---:|---:|
| 55–70 | 11 | 100.0% | +84.9% |
| 80–85 | 10 | 60.0% | +20.1% |
| 85–90 | 11 | 45.5% | **−14.7%** |
| 90+ | 2 | 100.0% | +88.6% |

**Role certainty:**

| Bucket | n | Hit | ROI |
|---|---:|---:|---:|
| 40–55 | 11 | 100.0% | +84.9% |
| 80–88 | 3 | 100.0% | +114.4% |
| **88–95** | **20** | **50.0%** | **−6.3%** |

Both fields run backwards. The 20 highest-role-certainty propositions went 10–10 for a negative return; the 11 lowest went 11–0.

### Market-family breakdown

| Market | n | Hit | ROI |
|---|---:|---:|---:|
| player_rush_yds | 4 | 100.0% | +86.8% |
| player_pass_attempts | 1 | 100.0% | +91.7% |
| player_pass_completions | 1 | 100.0% | +85.5% |
| player_receptions | 8 | 75.0% | +45.6% |
| player_reception_yds | 15 | 73.3% | +39.0% |
| player_rush_attempts | 2 | 50.0% | −11.8% |
| **player_pass_yds** | **3** | **0.0%** | **−100.0%** |

| Family | n | Hit | ROI |
|---|---:|---:|---:|
| Opportunity | 12 | 75.0% | +43.2% |
| Production | 22 | 68.2% | +28.8% |

| Side | n | Hit | ROI |
|---|---:|---:|---:|
| UNDER | 26 | 73.1% | +35.8% |
| OVER | 8 | 62.5% | +27.5% |

Opportunity markets outperformed production markets, consistent with the shorter causal chain thesis in the protocol. Passing yards was the only total wipeout.

### Verdict

**FAIL.** Conservative EV, confidence score and role certainty all failed to rank. The board's sort order added nothing on this slate, and its three primary ranking fields were all mildly inverted.

---

# PART II — WHY THE RANKING FAILED

The inversion is not random noise. It has a single identifiable cause.

**The model systematically under-allocates volume to high-usage players and over-allocates to the rest of the depth chart.** Because it under-forecasts the stars, its largest computed edges are concentrated in UNDERs on exactly the players whose usage it is most wrong about. High EV therefore *selects for* the model's own error.

Evidence:

| Player | Model | Market | Actual | Who was closer |
|---|---:|---:|---:|---|
| Stevenson rush attempts | 9.12 | 15.5 | **18** | Market |
| Stevenson RB-pool carry share | 42.2% | — | **75.0%** | Market |
| Smith-Njigba receptions | 3.88 | 6.5 | **8** | Market |
| Smith-Njigba rec yards | 52.47 | 81.5 | **122** | Market |

NE's modeled RB pool was Stevenson 9.12, Henderson 5.97, Gibson 3.94, Jennings 2.59. Henderson was inactive; Gibson and Jennings recorded nothing. Stevenson took 18 of 24 RB carries.

SEA's modeled backfield had Walker III at 9.87 and Charbonnet at 5.21. **Both recorded zero carries.** George Holani took 8 and had no model draws at all.

This produces the observed inversion mechanically:
- Highest EV → biggest model-market gap → concentrated in workhorse UNDERs → model wrong → losses at the top of the board.
- Lowest EV → small gaps on secondary players → model roughly right → wins at the bottom.

**The ranking is not broken. The ranking is faithfully sorting by the size of the model's own error.**

### The counter-evidence that must be preserved

On low-usage and bootstrap-role players the model **beat the market outright**: MAE 8.57 against 11.00, winning 5 of 8 head-to-head. A.J. Brown (model 29.3 vs market 64.5 vs actual 26) and Mack Hollins (model 34.2 vs market 9.5 vs actual 51) are the two cleanest cases. The model has real information about secondary-role usage. It does not have real information about workhorse concentration.

---

# PART III — BOARD IMPROVEMENTS FOR THE PYTHON PIPELINE

Ordered by expected impact. Each is specified as a concrete pipeline change.

## P0 — Blocking defects. Fix before the next slate.

### P0-1. Scheduled closing-line capture (new board)

**Problem:** zero true closes exist. CLV cannot be measured. The entire edge question is unanswerable.

**Change:** the pipeline must emit a scheduled snapshot series, not a single pre-kickoff render.

```
New artifact:  NFL_CLOSING_LINE_BOARD_YYYY-WXX.csv
Capture cadence per event: T-24h, T-6h, T-3h, T-60m, T-15m, T-5m
Terminal snapshot rule: last successful poll before market removal = TRUE_CLOSE
Required columns:
  candidate_id, event_id, player, market, side, line, bookmaker,
  american_odds, poll_timestamp_utc, minutes_to_kickoff,
  market_novig_prob, is_terminal_snapshot, close_quality_flag
```

Without this, every future audit degrades to the same DATA GAP. This is the highest-value single change in the list.

### P0-2. Starting-quarterback identity hard gate

**Problem:** the model simulated Sam Howell. Seattle started Sam Darnold, who left after five plays; Drew Lock finished 16/22 for 187 yards. Lock appears nowhere in the package — not the forecast board, not the role state, not the correlation matrix.

**Change:** abort the run, do not degrade it.

```
Pre-simulation gate:
  IF modeled_starting_qb != confirmed_depth_chart_qb_1 → RUN_ABORT: QB_IDENTITY_MISMATCH
  IF QB2 has no draws → emit QB_BACKUP_UNMODELED warning on the run manifest
New required artifact: NFL_QB_CONFIRMATION_YYYY-WXX.json
  {team, confirmed_starter, source, source_timestamp, modeled_starter, match: bool}
```

All 12 Darnold propositions were quarantined for the wrong reason — the entity layer had no draws, not because it knew he wasn't modeled.

### P0-3. Participation gate on forecast rows

**Problem:** 43 of 70 forecast rows belonged to players who recorded nothing (15 produced zero, 4 inactive). Their automatic UNDER wins inflated the headline directional hit rate from 44.4% to 68.6% — a 24-point illusion.

**Change:**

```
New column on all forecast boards: participation_confidence  [0-100]
New column: expected_snap_share, expected_snap_share_source
Gate: participation_confidence < 40 → forecast_gate = LOW_PARTICIPATION_EXCLUDE_FROM_CALIBRATION
Calibration weighting: rows with realized zero usage carry weight 0 in all
  directional accuracy and hit-rate statistics
```

Report two directional hit rates on every board, always: **all rows** and **participants only**. The second is the real number.

### P0-4. Inactives ingestion

**Problem:** a run labelled `WED_INACTIVES` contained no injury or inactives artifact, and Layer-1 was byte-identical to the eight-hour-older `WED_NOW` run. The label promised a state update that did not occur.

**Change:**

```
New required artifact: NFL_INACTIVES_YYYY-WXX.json
Gate: a run labelled *_INACTIVES MUST contain a non-empty inactives artifact,
      else RUN_ABORT: LABEL_STATE_MISMATCH
Gate: any player on the inactive list → all forecast rows suppressed, all market
      rows flagged PLAYER_INACTIVE, not silently priced
```

TreVeyon Henderson was inactive with four modeled rows carrying 5.97 rush attempts.

## P1 — Ranking and board-ordering defects.

### P1-1. Replace single-field EV sort with a composite rank

**Problem:** conservative EV has Spearman ρ = −0.05 against realized P/L. Sorting by it adds nothing.

**Change:** compute and surface a composite score, and keep raw EV as a displayed column rather than the sort key.

```
composite_rank_score =
      0.35 * normalized_conservative_ev
    + 0.25 * usage_concentration_agreement     (NEW — see P1-2)
    + 0.20 * participation_confidence
    + 0.10 * market_trust_score
    + 0.10 * cross_book_corroboration          (NEW — book_count normalized)

New board column: rank_basis  (which component dominated the score)
```

Retain `ev_conservative_pct` as a filter (must be > floor) but stop using it as the ordering key.

### P1-2. Usage-concentration agreement score (new field)

**Problem:** the single root cause of the ranking inversion. The model spreads volume evenly; real depth charts concentrate it.

**Change:**

```
New field on every candidate:
  usage_concentration_agreement =
    1 - |model_implied_team_share - market_implied_team_share|

Where market_implied_team_share is derived from the posted line relative to the
team volume total.

Gate: for any player at depth_rank 1 in their positional group, if
  model_implied_share < market_implied_share - 0.15
  → flag WORKHORSE_UNDERALLOCATION_RISK and apply an EV haircut
```

On this slate this single flag would have fired on Stevenson (42.2% modeled vs 75.0% actual) and Smith-Njigba, and would have suppressed 14 of the 15 losing model-side rows.

### P1-3. Recalibrate or invert `role_certainty_score`

**Problem:** role certainty is inversely related to accuracy. Rows at 88–95 went 10–10 for −6.3% ROI; rows at 40–55 went 11–0 for +84.9%.

**Change:** do not invert the field — that would be curve-fitting to n=1. Instead:

```
1. Decouple the two things the score currently conflates:
     role_stability_score   (how confident are we in the depth-chart slot)
     usage_precision_score  (how confident are we in the volume estimate)
   Current evidence: role stability was fine; usage precision was not.
2. Add column: prior_source and games_observed to every board row (already in
   role state, not surfaced on boards).
3. Suppress role_certainty from the ranking composite until n >= 5 slates of
   walk-forward evidence exists.
```

15 modeled skill players carried `prior_source = CURRENT_DEPTH_BOOTSTRAP` with `games_observed = 0`. That must be visible on the board face, not buried in a side artifact.

### P1-4. Direction-conditional disagreement filter

**Problem:** the 80-row `EXTREME_MODEL_MARKET_DISAGREEMENT` block returned +32.65% ROI on 40 model-side rows — statistically identical to the approved set's +33.03% on five times the volume. The filter removed edge.

But the losses were not random: **every losing row belonged to Stevenson, Smith-Njigba, or one Maye leg** — the exact workhorse-underallocation cases.

**Change:**

```
Replace the flat disagreement threshold with:

IF disagreement_direction == UNDER
   AND player.depth_rank == 1 in positional group
   AND WORKHORSE_UNDERALLOCATION_RISK flag set
   → BLOCK (this is the model being wrong)

ELSE IF disagreement is on a secondary/tertiary role player
   → DOWNGRADE to WATCH, do not block (model has demonstrated edge here)

Emit both paths to a new board: NFL_DISAGREEMENT_TRIAGE_BOARD_YYYY-WXX.csv
```

Applied retroactively to this slate, this rule blocks the 15 losers and releases the 25 winners.

## P2 — Distribution and entity quality.

### P2-1. Widen tails on production markets

Interval coverage on participants was 77.8% against a nominal 80% band — acceptable. Directional accuracy was 44.4% — not. Low bias (+0.13 mean error) with poor direction is the signature of a distribution centred correctly and too narrow.

```
Action: increase dispersion on production markets specifically
  (reception_yds, rush_yds, pass_yds) and re-check coverage.
Diagnostic to add: per-market interval coverage, not just aggregate.
Evidence: player_pass_yds went 0-3 for -100% ROI; the Maye 278.64 mean
  against a 178 actual was a 100.6-yard miss, 2x the market's 52.5 miss.
```

### P2-2. Entity-join hard fail

62 of 207 priced rows — **30% of the posted market** — were unpriceable for missing draws. Five players who produced meaningful statistics had no model opinion: Drew Lock (187 pass yards), George Holani (8 carries, 29 yards), Corey Kiner (6 carries), DeMario Douglas (5 receptions), AJ Barner (2 receptions). Elijah Arroyo's 0.5-receptions line at +185 was one of the two most extreme outcomes on the board and the model had no view.

```
Gate: missing_draw_rate > 20% of priced universe → RUN_STATUS = DEGRADED
      and suppress the EV board entirely rather than publishing a thin one.
New board column on all EV rows: priced_universe_coverage_pct
```

### P2-3. Correlation matrix coverage gate

The matrix covered 19 entities. Drake Maye and Hunter Henry — carrying 6 of 7 actionable rows between them — were absent. Correlation for the entire actionable cluster was DATA GAP.

```
Gate: any candidate appearing on the EV board MUST be present in the
      correlation matrix, else flag CORRELATION_UNMEASURED and cap that
      candidate's contribution to slate exposure.
```

## P3 — Board schema additions

Add to every EV and market-lined board:

```
participation_confidence
expected_snap_share
prior_source                        (e.g. CURRENT_DEPTH_BOOTSTRAP)
games_observed
usage_concentration_agreement
market_implied_team_share
model_implied_team_share
cross_book_corroboration            (book_count normalized 0-1)
composite_rank_score
rank_basis
priced_universe_coverage_pct
correlation_coverage_flag
```

Add two new boards:

```
NFL_CLOSING_LINE_BOARD_YYYY-WXX.csv          (P0-1)
NFL_DISAGREEMENT_TRIAGE_BOARD_YYYY-WXX.csv   (P1-4)
```

---

# PART IV — SLATE RESULT LEDGER

| Set | Rows | W–L | Units | ROI |
|---|---:|---|---:|---:|
| Tier 1 — Actionable | 7 | 5–2 | +2.312 | +33.03% |
| Tier 2 — Watchlist | 7 | 4–3 | +0.585 | +8.36% |
| Tier 3 — Market-lined consensus | 25 | 17–8 | directional | — |
| Blocked — model side | 40 | 28–12 | +13.059 | +32.65% |
| Blocked — best price dedupe | 26 | 19–7 | +10.037 | +38.60% |
| All model-side positive EV | 54 | 37–17 | +15.956 | +29.55% |
| Entity-failure universe (both sides) | 62 | 30–32 | −2.728 | — |

**Grading completeness:** 195 of 207 propositions graded; 12 DATA GAP (Maye and Shaheed rushing yards, V1 position scope, no totals supplied). 70 of 70 forecast rows graded.

### Forecast quality

| Population | Rows | Directional | Mean error | MAE | P10–P90 coverage |
|---|---:|---:|---:|---:|---:|
| All forecast rows | 70 | 68.6% | −10.54 | 15.95 | 72.9% |
| **Participants only** | **27** | **44.4%** | **+0.13** | **13.92** | **77.8%** |
| Non-participants | 43 | 83.7% | — | — | — |

---

# PART V — THE FIVE SEPARATE VERDICTS

1. **Forecast quality — FAIL on participants.** 44.4% directional. Mean bias near zero and coverage acceptable, so the centre is right and the shape is too tight.
2. **EV quality — FAIL.** Positive aggregate return with zero rank discrimination (ρ = −0.05). Return without ranking is not edge, it is a broadly soft board.
3. **CLV — FAIL, low confidence.** 0 for 3 on comparables, mean −2.63pp. No true closes. Unmeasurable at the required standard.
4. **Result — 5–2 on Tier 1, +2.312u hypothetical.** Noisiest signal in the file, least meaningful. Seven rows, three players, two theses.
5. **Process — PASS.** No gate overrides, no entries beyond hard stop, no fabricated fields, no correlated stacking. The pre-kickoff concentration warning (5 of 7 rows on Drake Maye) was correct and material: both losses came from that cluster.

---

# PART VI — WHAT WOULD CHANGE THE VERDICT

This is n=1. Nothing above is settled. The following would move it:

| Evidence needed | Slates | What it settles |
|---|---:|---|
| True closes captured at T-15m | 3 | Whether the desk beats the close at all |
| EV-rank monotonicity re-test | 5 | Whether the ranking has any discrimination |
| Usage-concentration flag backtest | 5 | Whether P1-2 fixes the inversion |
| Role-certainty sign test | 5 | Whether the inversion is structural or noise |
| Disagreement triage backtest | 8 | Whether P1-4 releases edge without releasing error |

**Do not tune thresholds on this slate.** Every number in Part I has n between 1 and 54 and most bucket cells hold fewer than 12 rows. The structural findings — workhorse underallocation, entity coverage, missing closes — are actionable now because they are mechanical failures, not statistical ones. The ranking and calibration findings are hypotheses that need four more slates.

---

# AUDIT CLOSE

```
============================================================
NFL — 2026 WEEK 01 — 2026-09-09 — NE @ SEA
AUDIT & CALIBRATION — DATASET_B_SEED_SLATE
============================================================
BEAT THE CLOSE:        UNPROVEN / LEANING FAIL  (0 of 3, no true closes)
PRICED CORRECTLY:      PARTIAL PASS  (Brier 0.2365 vs market 0.2528;
                       point-estimate MAE 13.98 vs market 12.14)
RANK DISCRIMINATION:   FAIL  (Spearman rho = -0.050, p = 0.777)
ROOT CAUSE:            WORKHORSE VOLUME UNDERALLOCATION
CAPITAL AT RISK:       0u — no authorization given
P0 FIXES OPEN:         4   (closing capture, QB gate, participation gate,
                            inactives ingestion)
P1 FIXES OPEN:         4   (composite rank, concentration score,
                            role-certainty decoupling, disagreement triage)
NEXT MEASUREMENT:      capture TRUE_CLOSE at T-15m on the next slate
============================================================
```

**Source note.** All model figures, IDs, reference prices and gates are read from the frozen handoff ZIPs `NFL-2026-W01-20260909T210629Z-WED_INACTIVES` and `NFL-2026-W01-20260909T130956Z-WED_NOW`. Player results and inactives are from the supplied capture package. Pre-kickoff market context and weather in Test 1 are from public editorial coverage dated 2026-09-08 and 2026-09-09 and are labelled as such; no figure in this document is estimated, interpolated, or inferred where evidence was unavailable — those cells read DATA GAP.
