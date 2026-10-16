# NFL PLAYER PROPS — FORMAL AUDIT & CALIBRATION REPORT
## League: NFL · Slate: 2026-09-14 · DEN @ KC · Week 1 Monday Night
### Controlling run: `NFL-2026-W01-20260914T220832Z-MNF_INACTIVES` · Model `0.3.0a4`

| Field | Value |
|---|---|
| League | NFL |
| Slate date (local) | 2026-09-14 |
| Kickoff (UTC) | 2026-09-15T00:15:00Z |
| Game | Denver Broncos at Kansas City Chiefs — GEHA Field at Arrowhead Stadium |
| Final score | **KC 31, DEN 10** — total 41, no overtime |
| Dataset A | FROZEN — handoff ZIP mounted and reconciled |
| Dataset B | ACCEPTED with 2 correctable defects |
| Report type | Postgame audit + calibration + pipeline patch specification |
| Real-money exposure | 0u — PAPER_ONLY throughout |

---

# PART 0 — THE CASINO-QUANT SCORE

Three questions were posed. Here are the three answers, stated before the evidence.

| # | Question | Verdict |
|---:|---|---|
| 1 | Did high-ranked model edge consistently **beat the close**? | **UNANSWERABLE — 0 qualifying closes captured. Objective failed.** |
| 2 | Did the model **price correctly**? | **PARTIAL FAIL.** Interval calibration passed (83.3% vs 80% target). Point calibration failed and the probability curve is inverted. |
| 3 | Did high-ranked edge **outperform lower-ranked edge**? | **YES at the claim level, NO at the row level.** Top-4 claims +75.0% ROI vs bottom-5 −62.6%. Across all 24 book rows, rank carries no signal (ρ=+0.259, p=0.22). |

**The headline finding is not any of the three.** It is that **10 of 26 modeled players never appeared on the official gamebook roster**, which invalidated the usage distribution the entire board was built on. That is a pipeline defect, not a modelling result, and it is fixed in Part 5.

---

# PART 1 — CLOSING LINE STATUS: FORMAL FAILURE NOTICE

## 1.1 What was captured

| Priority | Propositions | Qualifying closes | Status |
|---|---:|---:|---|
| P1 — Actionable | 24 | **0** | 24 exact-book DATA GAPs |
| P2 — Below gate | 14 | **0** | 14 exact-book DATA GAPs |
| P3 — Quarantine | 54 | **0** | Not attempted at scale |
| **Total** | **92** | **0** | — |

**Positive-CLV rate: 0/0 — NOT MEASURABLE. This is not 0%.**

## 1.2 Sourcing attempt and why it failed

A public search was run to recover closes. Result: **no qualifying source exists.**

| Source found | Why it does not qualify |
|---|---|
| FTN card, Bo Nix U34.5 pass attempts −105, timestamped 2026-09-14 16:36 ET | Timestamp is **1h33m earlier** than the pipeline's own reference snapshot (18:09 ET). A pre-reference observation cannot serve as a close. |
| Yahoo Sports: Walker O16.5 rec yds −115 DK; Engram O22.5 rec yds −113 FD | No timestamp. Published pregame, hours before kick. |
| Fanatics Sportsbook page: Dobbins +165, Walker −125 | Anytime-TD market. Not a market in this board. |
| LineTerminal per-player pages (Mims +142, Nix completions +101) | No source book identified, no UTC timestamp, no last-pre-kick flag. |
| VSiN / Bleacher Nation / SportsGrid previews | Editorial picks, not book price series. |

**Ruling: none of the above may be promoted to a close, and none is used for CLV anywhere in this report.** Media cards and aggregator pages are not closing-line evidence. Fabricating a close from them would corrupt every downstream calibration study built on this slate.

## 1.3 The structural cause

The pipeline captured its reference snapshot at **2026-09-14T22:09:04Z**, roughly **2 hours 6 minutes before kickoff**, and then stopped. Nothing in the architecture re-polls the market. A close that is not captured at the time cannot be reconstructed afterwards, because per-book, per-line prop price series are not publicly archived with book identity and timestamp.

**This is the second consecutive cycle where the CLV objective failed for the same reason.** It is the highest-priority patch in Part 5.

---

# PART 2 — DID HIGH-RANKED EDGE OUTPERFORM LOWER-RANKED EDGE?

This is the one casino-quant question the data can answer. It is answered two ways, and the two answers disagree — which is itself the finding.

## 2.1 Row level: NO SIGNAL

All 24 actionable book rows, split into terciles by conservative EV:

| Tercile | n | EV range | Win % | Mean ROI | Units |
|---|---:|---|---:|---:|---:|
| T1 — top 8 EV | 8 | 7.18 – 32.37 | 37.5% | −12.50% | −1.00u |
| T2 — middle 8 | 8 | 6.08 – 6.71 | 50.0% | +3.68% | +0.29u |
| T3 — bottom 8 | 8 | 4.04 – 6.05 | 37.5% | −32.94% | −2.64u |

```text
Spearman rank correlation, EV vs realized ROI  : rho = +0.259   p = 0.221   NOT SIGNIFICANT
Spearman rank correlation, EV vs win/loss      : rho = +0.140   p = 0.513   NOT SIGNIFICANT
```

**The EV ranking is non-monotonic at the row level.** The middle tercile was the only profitable one. The top tercile lost.

## 2.2 Claim level: MONOTONICITY HOLDS

Collapsing 24 book rows to the 9 independent claims (one best-priced expression per distinct thesis) changes the result completely.

| Rank | Claim | Proposition | Price | EV% | Result | Units |
|---:|---|---|---:|---:|---|---:|
| 1 | Mims role up | Mims O1.5 receptions (DK) | +125 | 12.44 | LOSS | −1.000 |
| 2 | Rice role down | Rice U4.5 receptions | +124 | 12.09 | **WIN** | +1.240 |
| 3 | Dobbins pass role down | Dobbins U0.5 receptions | +167 | 10.28 | **WIN** | +1.670 |
| 4 | Sutton role down | Sutton U3.5 receptions | +109 | 8.83 | **WIN** | +1.090 |
| 5 | Bryant production down | Bryant U26.5 rec yds | −113 | 7.21 | LOSS | −1.000 |
| 6 | Engram role down | Engram U2.5 receptions | +105 | 7.18 | LOSS | −1.000 |
| 7 | Worthy production down | Worthy U36.5 rec yds | −115 | 6.71 | **WIN** | +0.870 |
| 8 | KC pass volume up | Mahomes O223.5 pass yds | −112 | 6.56 | LOSS | −1.000 |
| 9 | DEN pass volume up | Nix O21.5 completions | −105 | 4.45 | LOSS | −1.000 |

| Cohort | Record | Units | ROI |
|---|---|---:|---:|
| **Top-4 EV claims** | 3-1 | **+3.000u** | **+75.0%** |
| **Bottom-5 EV claims** | 1-4 | **−3.130u** | **−62.6%** |
| All 9 claims | 4-5 | −0.130u | −1.45% |

**Interpretation.** The ranking works when the unit of analysis is a distinct claim. It disappears when duplicate book rows and adjacent lines are treated as independent observations, because duplicates cluster inside whichever claim happens to be wrong — here, four Mahomes rows and two Nix rows all expressing one losing view of the game total.

**Consequence for the pipeline: the EV board's ranking unit is wrong.** It ranks rows. It must rank claims, with rows nested underneath as execution options.

## 2.3 Tier ladder: did the gates separate anything?

| Tier | n | Win % | Mean ROI | Units |
|---|---:|---:|---:|---:|
| Tier 1 — ACTIONABLE (EV above family gate) | 24 | 41.7% | −13.92% | −3.341u |
| Tier 2 — BELOW_GATE (0 < EV < gate) | 14 | 35.7% | −32.27% | −4.519u |
| Tier 3 — QUARANTINE (extreme disagreement) | 15 | 46.7% | n/a — no prices released | n/a |

**The EV gate separated Tier 1 from Tier 2 in the correct direction**, by 6.0 points of hit rate and 18.4 points of ROI. That is the one gate on the slate that demonstrably earned its place.

**The disagreement gate did not.** Tier 3 posted the *highest* raw directional hit rate of any tier while being blocked entirely. Detail:

| Quarantine blocked | Outcome |
|---|---|
| Walker U16.5 rush att (actual 23), U63.5 rush yds (actual 173) | **Saved you — two catastrophic losses** |
| Mims O10.5 rec yds (0), Nix O225.5 pass yds (131), Bryant U2.5 rec (4), Kelce U42.5 rec yds (71) | Saved you — four more losses |
| Waddle U4.5 rec (1), U58.5 rec yds (2) | **Cost you — two large winners** |
| Worthy U3.5 rec (3), Kelce U4.5 rec (3), Dobbins U11.5 rush att (8) | Cost you — three more winners |

Net 7-8. **The disagreement gate is a filter for disagreement, not for model error, and on this slate it cut both ways at roughly equal rates.**

## 2.4 The one-sided quote cohort: decisive

| Anchor status | n | Mean EV% | Win % | Units |
|---|---:|---:|---:|---:|
| **ONE_SIDED** (no no-vig anchor) | 3 | **14.61** | **0.0%** | **−3.000u** |
| TWO_SIDED (anchored) | 21 | 6.86 | 47.6% | −0.336u |

**The entire actionable loss on this slate is the three one-sided rows.** They carried more than double the mean EV of their anchored peers and went 0-3. Remove them and the actionable board is essentially flat.

n=3. This is not proof. It is exactly the pattern predicted at board-render time — when `p_blend` has no market anchor to shrink toward, the model's unshrunk probability flows straight into EV and inflates it. **Treat as confirmed-pending-replication and patch now.**

## 2.5 Market family

| Tier | Family | n | Win % | Units |
|---|---|---:|---:|---:|
| ACTIONABLE | Opportunity (receptions, attempts, completions) | 15 | 40.0% | −1.84u |
| ACTIONABLE | Production (yards) | 9 | 44.4% | −1.51u |
| BELOW_GATE | Opportunity | 5 | **0.0%** | −5.00u |
| BELOW_GATE | Production | 9 | 55.6% | +0.48u |

The opportunity-market priority in the protocol is **not supported by this slate's betting record** — though it is strongly supported by the forecast-error record in Part 3. Those two facts are reconciled in Part 4.

---

# PART 3 — CALIBRATION

42 of 70 forecast rows were gradeable. The other 28 are covered in Part 4.

## 3.1 Interval calibration: PASS

```text
P10–P90 coverage: 35 / 42 = 83.3%    target 80%    PASS
```

Seven exceptions:

| Player | Stat | Actual | P10 | P90 | Direction |
|---|---|---:|---:|---:|---|
| Kenneth Walker III | rushing yards | 173 | 6 | 56 | ABOVE |
| Kenneth Walker III | rushing attempts | 23 | 5 | 11 | ABOVE |
| Travis Kelce | receiving yards | 71 | 7 | 68 | ABOVE |
| Emmett Johnson | receiving yards | 44 | 0 | 18 | ABOVE |
| Emmett Johnson | rushing attempts | 8 | 1 | 5 | ABOVE |
| Bo Nix | passing yards | 131 | 191 | 420 | BELOW |
| Jaylen Waddle | receiving yards | 2 | 4 | 65 | BELOW |

Five of seven are KC skill players breaking the **ceiling**. That is the roster-gap signature, not a width problem. The intervals are correctly sized; the central tendencies were fed bad inputs.

## 3.2 Point calibration: FAIL — curve is inverted

| Model probability bucket | n | Model says | Actually hit | Delta |
|---|---:|---:|---:|---:|
| 50–55% | 16 | 52.7% | **75.0%** | +22.3 |
| 55–60% | 10 | 58.0% | **80.0%** | +22.0 |
| 60–65% | 13 | 62.2% | **53.8%** | −8.4 |
| 65–70% | 3 | 65.8% | **33.3%** | −32.5 |

**The model was most accurate where it was least confident and least accurate where it was most confident.** With n=42 across four buckets this is not statistically significant, but it is the exact opposite of a well-calibrated curve and it is directionally consistent with the EV-rank result in 2.1.

Overall directional record on graded forecast rows: **28-14, 66.7%.**

## 3.3 Point error by market family

| Market | n | MAE | Bias (actual − model) |
|---|---:|---:|---:|
| **receptions** | 14 | **1.56** | **−0.17** |
| rushing_attempts | 4 | 6.25 | +4.03 |
| completions | 2 | 7.08 | −7.08 |
| passing_attempts | 2 | 9.93 | −9.93 |
| receiving_yards | 14 | 24.53 | −6.35 |
| rushing_yards | 4 | 41.33 | +35.50 |
| **passing_yards** | 2 | **127.68** | **−127.68** |

**Receptions was the only clean market.** MAE 1.56, bias −0.17 — essentially unbiased. This is the opportunity-market thesis validating exactly as designed: shortest causal chain, smallest error.

**Passing yards was off by 128 yards per quarterback, both in the same direction.** Every passing OVER on the board descended from that single failure.

## 3.4 Game environment: the root cause of the passing cluster

| Metric | Model | Market reference | Actual | Model error | Market error |
|---|---:|---:|---:|---:|---:|
| Total points | 46.88 | 42.5 | **41** | **−5.88** | −1.50 |
| DEN offensive plays | 62.88 | — | 47 | −15.88 | — |
| KC offensive plays | 59.59 | — | 67 | +7.41 | — |
| Bo Nix passing yards | 299.82 | — | 131 | −168.82 | — |
| Mahomes passing yards | 270.55 | — | 184 | −86.55 | — |

**The market's total was four times more accurate than the model's.** The model priced this game +4.38 points above the market and the game landed 1.5 points *below* the market. Every pass-volume and pass-production OVER inherited that error. All of them lost.

---

# PART 4 — ROOT CAUSE: THE ROSTER FAILURE

## 4.1 Scale

**10 of 26 modeled players never appeared on the official gamebook roster. 28 of 70 forecast rows are ungradeable.**

```text
DEN : Blake Watson · Dane Key · Jaleel McLaughlin · Kolbe Katsis
KC  : Isiah Pacheco · Kareem Hunt · Marquise Brown · Andrew Armstrong
      Jeff Caldwell · Jimmy Holiday
```

## 4.2 Mechanism

The slate was labelled `MNF_INACTIVES`. The handoff shipped **no inactives artifact**. Every modeled player carried `availability_status = ACTIVE_OR_UNLISTED` — a default, not a confirmation. The usage model then distributed a full team's touches across ten players who did not play, mechanically suppressing the projections of every player who did.

## 4.3 The clearest casualty

| | Model | Market line | Actual |
|---|---:|---:|---:|
| Kenneth Walker III rushing attempts | 7.62 | 16.5 | **23** |
| Kenneth Walker III rushing yards | 30.52 | 63.5 | **173** |

The model gave Walker 7.6 carries because it split the KC backfield with Pacheco and Hunt. **Neither was on the roster.** Walker took the entire workload.

The board run attributed this to Walker's `CURRENT_DEPTH_BOOTSTRAP` prior (zero observed games). **That diagnosis was wrong, or at best incomplete.** The bootstrap prior was a contributing factor; the proximate cause was a depth chart populated with absent players. A perfect prior for Walker would still have been diluted by two phantom backs.

## 4.4 Reconciling 2.5 with 3.3

Opportunity markets showed the **lowest forecast error** (receptions MAE 1.56) and the **worst betting record** (below-gate opportunity 0-5). These are consistent: the receptions *distributions* were well-shaped, but the *level* was shifted by the phantom-player dilution. A well-shaped distribution centred in the wrong place produces small absolute errors on low-magnitude stats and still loses bets clustered near the line.

---

# PART 5 — PIPELINE PATCH SPECIFICATION

Eight patches, ordered by expected value. Each carries an acceptance test.

## PATCH-01 — Close capture daemon `[P0 — BLOCKING]`

**Problem.** Reference snapshot at kickoff −2h06m, then nothing. Two consecutive cycles with CLV unmeasurable.

**Change.** Add a scheduled re-poll of every released candidate at **kickoff −5 minutes**, writing `NFL_CLOSE_SNAPSHOT_<slate>.csv` with `candidate_id, book, line, american_odds, captured_at_utc, minutes_to_kickoff, two_sided_flag`. Fall back to −15m and −30m captures; label each with its own `close_quality_flag`.

**If self-hosting is not viable**, procure per-book closing odds from a provider that stores them natively — SportsGameOdds (`includeOpenCloseOdds=true`), Odds-API.io (`/v3/historical/closing-lines`), or PropLine (`/closing`). Public media pages are not an acceptable substitute and must be rejected by the ingest.

**Acceptance test:** ≥90% of released candidates carry a `TRUE_CLOSE` or `NEAR_CLOSE_PROXY` flag on the next slate. Below that, the slate is marked CLV-UNGRADEABLE at render time, not discovered afterwards.

## PATCH-02 — Fail the run on missing availability artifact `[P0 — BLOCKING]`

**Problem.** A slate labelled `*_INACTIVES` shipped without an inactives file and produced 28 forecast rows for absent players.

**Change.** Handoff build fails if any of these is true:
- slate label contains `INACTIVE` and no inactives artifact is present;
- any modeled player's `availability_status` is the default `ACTIVE_OR_UNLISTED` and kickoff is under 4 hours away;
- modeled roster size exceeds confirmed active roster size for either team.

**Acceptance test:** zero rows with `gamebook_status = NOT_ON_OFFICIAL_GAMEBOOK_ROSTER` on the next three slates.

## PATCH-03 — Rank claims, not rows `[P1]`

**Problem.** EV rank has no predictive signal across 24 rows (ρ=+0.259, p=0.22) but strong separation across 9 claims (+75.0% vs −62.6%).

**Change.** The EV board's primary key becomes `thesis_id + player + stat + side`. Book rows nest beneath as execution options with a `best_price` marker. Emit `claim_rank`, `claim_count`, and `rows_in_claim`. Report the claim record as the headline; the row record becomes a sub-table.

**Acceptance test:** EV board top-level row count equals distinct claim count. Duplicate book rows never appear as separate ranked entries.

## PATCH-04 — Reject or haircut one-sided quotes `[P1]`

**Problem.** One-sided rows carried 14.61% mean EV vs 6.86% for anchored rows and went 0-3.

**Change.** Where `market_novig_prob` is null, `p_blend` must not default to `p_calibrated`. Either:
- **(a)** shrink toward the cross-book consensus no-vig for the same proposition at other books, where one exists; or
- **(b)** where no anchor exists at any book, set `model_status = PAPER_ONLY` and exclude from the actionable board.

Never release a row whose EV advantage over its own two-sided twin exceeds 5 percentage points at the same line and price.

**Acceptance test:** the Mims case cannot recur — identical line and price at two books must not produce EVs of 32.37% and 12.44%.

## PATCH-05 — Replace the symmetric disagreement gate `[P1]`

**Problem.** The gate blocked 7 winners and 8 losers. It filters disagreement, not error.

**Change.** Condition the block on **why** the model disagrees, not on the size of the gap:

| Condition | Action |
|---|---|
| `games_observed = 0` or `prior_source = CURRENT_DEPTH_BOOTSTRAP` | **BLOCK** — model has no basis |
| Roster/availability unconfirmed | **BLOCK** — inputs unreliable |
| Full observed history, role certainty ≥ 87, gap > 18pp | **RELEASE as PAPER_ONLY** and log for calibration |
| Gap > 18pp with no identifiable cause | **WATCH** — do not block outright |

**Acceptance test:** blocked-cohort hit rate falls materially below released-cohort hit rate. On this slate the blocked cohort *beat* the released cohort (46.7% vs 41.7%) — that must invert.

## PATCH-06 — Propagate game-total disagreement into position sizing `[P2]`

**Problem.** The model's +4.38-point total disagreement drove every passing OVER. Four Mahomes rows and two Nix rows were one bet.

**Change.** Compute `game_total_disagreement_pts`. Where it exceeds 3.0, tag every pass-volume and pass-production candidate in that game with `SHARED_ROOT_EXPOSURE = GAME_TOTAL` and cap their combined notional at one claim's worth. Surface the disagreement on the game board at render time.

**Acceptance test:** no slate releases more than one independently-sized claim per shared root exposure.

## PATCH-07 — Complete the correlation matrix `[P2]`

**Problem.** The 80×80 matrix omits Bo Nix entirely, plus Mims, Engram, Bryant, Franklin, Key, Katsis, and **all DEN rushing series**. Six of 17 actionable propositions could not be correlation-priced, which made the best available SGP structure (Nix attempts + completions, the DEN analogue of the Mahomes stack) impossible to build.

**Change.** The matrix must span every modeled player × every modeled stat. Emit `correlation_coverage_pct` in the manifest and fail the handoff below 100% for released candidates.

**Acceptance test:** every actionable candidate has correlation rows against every other actionable candidate in the same game.

## PATCH-08 — Separate calibration cohorts at write time `[P3]`

**Change.** Stamp each forecast row with `prior_cohort ∈ {OBSERVED_HISTORY, BOOTSTRAP}` and `availability_confirmed ∈ {TRUE, FALSE}`. All calibration reporting buckets on these. Mixing a zero-games bootstrap player into the calibration curve contaminates it in both directions.

**Acceptance test:** calibration tables refuse to render a combined curve without the cohort split.

---

# PART 6 — DATASET B PACKAGE QC

| Check | Result |
|---|---|
| 38 rows matched to Dataset A by `candidate_id` | 38/38, zero unmatched |
| Book / side / line / reference odds / `p_conservative` / fair odds / EV% / buy-to / hard-stop | All reconcile exactly |
| Paper grades independently recomputed from actuals | **38/38 correct** |
| `theoretical_roi_at_reference_pct` recomputed | **38/38 correct** |
| Forecast 70: side, line, probability, mean, P10, P90 vs Dataset A | **70/70 match** |
| Forecast 70: grades and `mean_error` recomputed | **42/42 graded rows correct** |
| Fabricated closes, prices, books, or timestamps | **None found** |

**Defect 1.** Mahomes `pass_yds` rows `5D9CAC3D`, `B0990AB0`, `F59FD0A0` record `minimum_required_ev_pct = 3.5`; Dataset A says **4.5**. No verdict change (EVs 6.56 / 6.11 / 4.52 all clear 4.5). Field is wrong and would corrupt threshold research.

**Defect 2.** All 14 below-gate rows record `reference_timestamp = DATA GAP`. Dataset A has every one (`2026-09-14T22:09:04Z` or `:05Z`). Honest fail-closed call made without the ZIP; recoverable.

**Commended:** the package refused to promote four LineTerminal observations into closes. That is correct and this audit upholds it.

---

# PART 7 — LEDGER

```text
============================================================
NFL PLAYER PROPS — SLATE LEDGER 2026-09-14 DEN @ KC W01
============================================================
FINAL                        KC 31, DEN 10 — total 41
MODEL TOTAL                  46.88   (error −5.88)
MARKET TOTAL                 42.5    (error −1.50)

FORECAST ROWS                70 issued / 42 graded / 28 ungradeable
DIRECTIONAL RECORD           28-14 (66.7%)
P10–P90 COVERAGE             83.3%  vs 80% target   PASS
POINT CALIBRATION            INVERTED               FAIL
RECEPTIONS MAE               1.56  bias −0.17       PASS
PASSING YARDS MAE            127.68 bias −127.68    FAIL

ACTIONABLE ROWS              24 · 10-14 · −3.341u · −13.92%
  two-sided (21)             10-11 · −0.336u
  one-sided  (3)             0-3   · −3.000u
BELOW GATE                   14 ·  5-9  · −4.519u · −32.27%
QUARANTINE (15 sampled)      7-8 · no prices released
INDEPENDENT CLAIMS           9  ·  4-5  · −0.130u · −1.45%
  top-4 EV                   3-1 · +3.000u · +75.0%
  bottom-5 EV                1-4 · −3.130u · −62.6%

CLOSES CAPTURED              0 of 92
POSITIVE CLV RATE            NOT MEASURABLE (0/0)
REAL-MONEY EXPOSURE          0u — PAPER_ONLY
============================================================
```

---

# PART 8 — STATISTICAL DISCLAIMER

One game. Nine independent claims. Forty-two graded forecast rows. Three one-sided quotes. Fifteen sampled quarantine propositions.

**Nothing in this report confirms or refutes the model.** No p-value here clears conventional significance and none is claimed to.

What this slate produces is:

1. **Two process defects that are certain and immediately actionable** — the missing availability artifact (PATCH-02) and the absent close capture (PATCH-01). Neither is a statistical inference. Both are observed facts about the pipeline.
2. **Four hypotheses worth tracking across the season** — the one-sided EV inflation, the inverted probability curve, the claim-vs-row ranking result, and the symmetric disagreement gate's failure to discriminate.

Promote a hypothesis to a rule only after it holds across a minimum of **50 independent claims** and **200 graded forecast rows**. Until then these are logged observations, not calibration evidence.

---

# FILE NAMING CONVENTION

One file per league per slate. This report is:

```text
NFL_PLAYER-PROPS_AUDIT-CALIBRATION_2026-09-14_DEN-at-KC_W01.md
```

Pattern:

```text
<LEAGUE>_<MARKET-CLASS>_AUDIT-CALIBRATION_<YYYY-MM-DD>_<SLATE-ID>_<PERIOD>.md
```

| Token | Rule |
|---|---|
| `<LEAGUE>` | `NFL`, `NCAAF`, `NBA`, `WNBA`, `MLB`, `NHL`, `EPL`, `LOL` — never combined in one file |
| `<MARKET-CLASS>` | `PLAYER-PROPS`, `TOTALS`, `SURVIVOR`, `TD-SCORER`, `PITCHER-K` |
| `<YYYY-MM-DD>` | Slate date in the venue's local date, not UTC |
| `<SLATE-ID>` | `DEN-at-KC` for single-game; `FULL-SLATE` or `EARLY-WINDOW` for multi-game |
| `<PERIOD>` | `W01`, `RS`, `PO` |

**Never merge leagues into one file. Never merge slates into one file.** Each slate's audit is a standalone calibration record and must remain independently citable.

---

**Report status:** FINAL · Dataset A frozen and reconciled · Dataset B accepted with 2 correctable defects · CLV objective FAILED · Real-money authorization BLOCKED · Stake 0u
