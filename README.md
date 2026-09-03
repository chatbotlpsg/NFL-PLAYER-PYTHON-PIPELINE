# AITA NFL Opportunity-First Player Alpha Pipeline

Version: `0.3.0a3`  
Season target: NFL 2026  
Production doctrine: **Model opportunity first. Model production second. Price the market third. Trade outside Python.**

## Architecture lock

```text
NFLVERSE / NFLREADPY        historical football backbone
ESPN JSON adapter           current slate / roster / depth / injury state
NWS                         outdoor weather
The Odds API                current model-reference market pricing only
        ↓
TEAM STATE
        ↓
TEAM PLAYS
        ↓
PASS / RUN
        ↓
QB / RB / RECEIVER OPPORTUNITY
        ↓
PLAYER PRODUCTION
        ↓
JOINT MONTE CARLO
        ↓
RAW → CALIBRATED → BLENDED → CONSERVATIVE PROBABILITY
        ↓
FAIR ODDS / EV / BUY-TO / HARD STOP
        ↓
CORRELATION / THESIS OPTIMIZER / BOARDS
        ↓
IMMUTABLE NFL TRADING-AGENT HANDOFF ZIP
        ↓
PYTHON ENDS
```

The production package intentionally contains **no** closing-line watcher, actual-entry tracker, play grader, CLV producer, or post-handoff trading-history writer. Dataset B belongs to the separate Claude NFL Trading Agent. A research-only importer may read completed Dataset B later for calibration.

## V1 market scope

Opportunity markets:

- `player_receptions` — WR/TE/RB receptions
- `player_rush_attempts` — RB carries
- `player_pass_attempts` — QB attempts
- `player_pass_completions` — QB completions

Production derivatives:

- `player_reception_yds`
- `player_rush_yds`
- `player_pass_yds`

Mainline anchor context:

- `h2h`
- `spreads`
- `totals`

Not in V1: TD props, first TD, longest play, defensive props, kickers, alternate props, SGP optimization, live betting, futures.

## Installation — Git Bash on Windows

Assuming this repository is at `C:\Python\NFL_MODEL`:

```bash
cd /c/Python/NFL_MODEL
python -m venv virt
source virt/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp -n .env.example .env
```

Edit `.env` and set:

```text
ODDS_API_KEY=YOUR_KEY_HERE
NWS_USER_AGENT=AITA-NFL-MODEL/0.3.0a3 (contact: your-email@example.com)
```

Never commit `.env`.

## Validation

```bash
cd /c/Python/NFL_MODEL
source virt/Scripts/activate
python -m pytest -q
python -m nfl_model --root . validate-config --season 2026 --week 1
python -m nfl_model --root . odds-plan --season 2026 --week 1 --events 16 --shortlist-events 6
```

Expected 16-game planning maximum with three books:

```text
Mainlines                  3
Opportunity full slate    64
Targeted yardage          18
Candidate reprice         12
-----------------------------
Planned max               97 credits
```

## Offline end-to-end proof

This uses frozen synthetic football and odds inputs. It consumes zero Odds API credits.

```bash
python -m nfl_model --root . demo --season 2026 --week 1 --draws 25000
```

It must create an immutable ZIP under:

```text
data/outputs/NFL_TRADING_AGENT_HANDOFF_2026-W01_*.zip
```

## Live production run

```bash
python -m nfl_model --root . run \
  --season 2026 \
  --week 1 \
  --mode production \
  --shortlist-events 6
```

The live run performs the locked order:

1. ESPN slate.
2. ESPN current roster/depth/injury snapshots.
3. nflverse historical cache and states.
4. NWS weather only where relevant.
5. Independent shared game-state + joint player simulation before prop pricing.
6. Free Odds API event discovery.
7. 3-credit mainline anchor pull and bounded score/game-script re-simulation.
8. Four-market opportunity prop pull.
9. Opportunity pricing and shortlist.
10. Yardage pull only for shortlisted events.
11. Conservative EV and guardrails.
12. Limited final candidate reprice.
13. Boards, correlation, thesis optimization.
14. Deterministic handoff ZIP.
15. Python stops.

## Stage commands

```bash
python -m nfl_model --root . ingest-football --season 2026 --week 1
python -m nfl_model --root . simulate --season 2026 --week 1 --draws 50000
python -m nfl_model --root . odds-plan --season 2026 --week 1 --events 16 --shortlist-events 6
python -m nfl_model --root . fetch-mainlines --season 2026 --week 1
```

Paid event-level prop calls require explicit event IDs when run manually:

```bash
python -m nfl_model --root . fetch-opportunity-odds \
  --season 2026 --week 1 \
  --event-id ODDS_API_EVENT_ID

python -m nfl_model --root . fetch-shortlist-yardage \
  --season 2026 --week 1 \
  --event-id ODDS_API_EVENT_ID

python -m nfl_model --root . reprice \
  --season 2026 --week 1 \
  --event-id ODDS_API_EVENT_ID \
  --market player_receptions
```

## Handoff contract

Every production handoff includes the model-reference market snapshot (Dataset A), the four probability layers, fair prices, four EV layers, BUY-TO/hard-stop guidance, uncertainty, correlation, thesis information, provider health, quota report, lineage, and run manifest.

It does **not** contain actual entries, closing lines, grades, CLV, or trading history.

If football information materially changes after freeze, create a new Python run. Do not let the Trading Agent invent a replacement probability.

## Provider notes

- ESPN endpoints are treated as unsupported interfaces and isolated under `providers/espn/`.
- nflreadpy is loaded lazily and cached in Parquet.
- NWS point-to-hourly lookup is used only for relevant stadiums.
- The Odds API request fingerprint, TTL cache, quota ledger, reserve gate, and response headers are centralized under `providers/odds_api/`.

## Raw-data policy

```text
data/raw        append-only provider snapshots and quota ledger
data/normalized reproducible normalized tables
data/features   reproducible simulation/features
data/cache      provider caches
data/outputs    immutable run directories + handoff ZIPs
```

Do not manually edit raw provider responses.

## v0.3.0a3 — Full Slate Forecast Board Architecture

Every simulation now produces **market-blind calibration forecast boards** in addition to the existing price-sensitive EV boards:

- `NFL_RECEIVING_FORECAST_BOARD_<season>-W<week>.csv`
- `NFL_RUSHING_FORECAST_BOARD_<season>-W<week>.csv`
- `NFL_PASSING_FORECAST_BOARD_<season>-W<week>.csv`
- `NFL_ALL_PLAYER_FORECAST_BOARD_<season>-W<week>.csv`

Each modeled player/stat row contains the full Monte Carlo distribution (`mean`, `median`, P10/P25/P75/P90), a model-native half-point calibration reference line, raw OVER and UNDER probabilities, the model's most-probable side, fair odds for that side, role certainty, and a stable calibration key.

The handoff also contains **Market-Lined Pick Boards**. These select the model's more probable OVER/UNDER side at the consensus posted sportsbook line whether or not the price clears the EV threshold. This keeps three concepts separate:

1. **Full Forecast Board** — football-model forecast/calibration universe; market-blind and not a bet recommendation.
2. **Market-Lined Pick Board** — most probable side at an actual posted line; probability-first and not EV-filtered.
3. **EV Play Board** — price-sensitive actionable plays that clear conservative EV requirements.

`simulate` preserves every Layer-1 board run in an immutable `forecast_snapshots/<snapshot_id>/` directory while also updating convenient latest-copy CSVs. Actual results, grading, closing lines and CLV remain Dataset-B responsibilities of the separate NFL Trading Agent.

Production simulation count is locked to **500,000 draws** unless explicitly overridden for development/testing.
