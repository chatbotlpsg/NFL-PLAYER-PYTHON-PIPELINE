# AITA NFL Player Prop Model — Windows Git Bash Install / Replace Commands

Final source ZIP:

```text
NFL-PLAYER-PROP-MODEL-AITA-2026-OPPORTUNITY-FIRST-V1-FULL.zip
```

Assumption: manually move the downloaded ZIP into `C:\Python` first.

## 1. Back up the current NFL model and unpack the new build

```bash
cd /c/Python

ZIP="NFL-PLAYER-PROP-MODEL-AITA-2026-OPPORTUNITY-FIRST-V1-FULL.zip"
test -f "$ZIP" || { echo "ERROR: $ZIP not found in C:/Python"; exit 1; }

STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP=""
if [ -d NFL_MODEL ]; then
  BACKUP="NFL_MODEL_BACKUP_${STAMP}"
  mv NFL_MODEL "$BACKUP"
  echo "Backed up old model to C:/Python/$BACKUP"
fi

mkdir -p NFL_MODEL
unzip -o "$ZIP" -d NFL_MODEL
cd /c/Python/NFL_MODEL
```

## 2. Rebuild the virtual environment

```bash
cd /c/Python/NFL_MODEL
python -m venv virt
source virt/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## 3. Restore or create `.env`

```bash
cd /c/Python/NFL_MODEL

if [ -n "$BACKUP" ] && [ -f "/c/Python/$BACKUP/.env" ]; then
  cp "/c/Python/$BACKUP/.env" .env
else
  cp -n .env.example .env
fi

notepad .env
```

Required secret:

```text
ODDS_API_KEY=YOUR_KEY_HERE
```

Recommended NWS user-agent:

```text
NWS_USER_AGENT=AITA-NFL-MODEL/0.3.0a3 (contact: your-email@example.com)
```

Never commit `.env` and never put the key in the handoff ZIP.

## 4. Validate the new build

```bash
cd /c/Python/NFL_MODEL
source virt/Scripts/activate

python -m pytest -q
python -m nfl_model --root . validate-config --season 2026 --week 1
python -m nfl_model --root . odds-plan --season 2026 --week 1 --events 16 --shortlist-events 6
```

Expected test result for this packaged build:

```text
19 passed
```

Expected Week-1 16-game quota plan:

```text
Mainline cost:                        3
Opportunity full-slate maximum:      64
Targeted yardage allowance:          18
Final candidate reprice allowance:   12
Planned maximum:                     97 credits
Safety reserve:                     100 credits
```

## 5. Run the zero-credit end-to-end proof

```bash
python -m nfl_model --root . demo --season 2026 --week 1 --draws 25000
```

This uses frozen synthetic data and spends zero Odds API credits. It must create an immutable handoff ZIP under `data/outputs/`.

## 6. Run football data / simulation stages separately

```bash
python -m nfl_model --root . ingest-football --season 2026 --week 1
python -m nfl_model --root . simulate --season 2026 --week 1 --draws 50000
```

## 7. First real production run

Only after `.env` contains a valid `ODDS_API_KEY`:

```bash
python -m nfl_model --root . run \
  --season 2026 \
  --week 1 \
  --mode production \
  --shortlist-events 6
```

Production defaults to 100,000 Monte Carlo draws. The Python process ends after it writes the immutable NFL Trading-Agent handoff ZIP.

## 8. Audit a produced handoff directory

Replace the run directory with the one printed by your production run:

```bash
python -m nfl_model --root . audit \
  --season 2026 \
  --week 1 \
  --run-dir "data/outputs/YOUR_RUN_ID_HERE"
```

Expected:

```json
{
  "status": "OK",
  "missing": [],
  "forbidden_post_handoff_artifacts": []
}
```
