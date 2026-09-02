from __future__ import annotations

from typing import Any
import pandas as pd

from nfl_model.ids.events import make_event_id
from nfl_model.ids.teams import canonical_team


def normalize_scoreboard(payload: dict, season: int, week: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for event in payload.get("events", []):
        competitions = event.get("competitions") or []
        if not competitions:
            continue
        comp = competitions[0]
        teams: dict[str, dict] = {}
        for c in comp.get("competitors", []):
            t = c.get("team", {})
            teams[c.get("homeAway", "")] = {
                "id": str(t.get("id", "")),
                "abbr": canonical_team(t.get("abbreviation", "")),
                "name": t.get("displayName") or t.get("name"),
            }
        if "home" not in teams or "away" not in teams:
            continue
        kickoff = event.get("date")
        home, away = teams["home"], teams["away"]
        rows.append({
            "aita_event_id": make_event_id(season, week, kickoff, away["abbr"], home["abbr"]),
            "season": season,
            "week": week,
            "kickoff_utc": kickoff,
            "home_team": home["abbr"],
            "away_team": away["abbr"],
            "home_espn_team_id": home["id"],
            "away_espn_team_id": away["id"],
            "espn_event_id": str(event.get("id", "")),
            "status": ((event.get("status") or {}).get("type") or {}).get("name"),
            "venue": ((comp.get("venue") or {}).get("fullName")),
        })
    return pd.DataFrame(rows)


def normalize_roster(payload: dict, team: str) -> pd.DataFrame:
    rows = []
    groups = payload.get("athletes", [])
    for group in groups:
        items = group.get("items") or []
        if not items and isinstance(group, dict) and group.get("id"):
            items = [group]
        for athlete in items:
            pos = athlete.get("position") or {}
            rows.append({
                "espn_athlete_id": str(athlete.get("id", "")),
                "full_name": athlete.get("fullName") or athlete.get("displayName"),
                "position": pos.get("abbreviation") if isinstance(pos, dict) else None,
                "current_team": canonical_team(team),
                "jersey": athlete.get("jersey"),
                "active_flag": athlete.get("status", {}).get("type") != "inactive" if isinstance(athlete.get("status"), dict) else True,
            })
    return pd.DataFrame(rows)


def normalize_depth_chart(payload: dict, team: str) -> pd.DataFrame:
    rows = []
    for chart in payload.get("depthCharts", []):
        unit = chart.get("name")
        for _, position in (chart.get("positions") or {}).items():
            p = position.get("position") or {}
            pos = p.get("abbreviation") or p.get("name")
            for item in position.get("athletes", []):
                athlete = item.get("athlete") or item
                rows.append({
                    "team": canonical_team(team),
                    "unit": unit,
                    "position": pos,
                    "rank": item.get("rank"),
                    "espn_athlete_id": str(athlete.get("id", "")),
                    "player_name": athlete.get("displayName") or athlete.get("fullName"),
                })
    return pd.DataFrame(rows)


def normalize_injuries(payload: dict, team: str | None = None) -> pd.DataFrame:
    rows = []
    groups = payload.get("injuries") or payload.get("items") or []
    if isinstance(groups, dict):
        groups = [groups]
    for item in groups:
        athlete = item.get("athlete") or {}
        status = item.get("status")
        rows.append({
            "team": canonical_team(team or ((item.get("team") or {}).get("abbreviation", ""))),
            "espn_athlete_id": str(athlete.get("id", "")),
            "player_name": athlete.get("displayName") or athlete.get("fullName"),
            "status": status.get("name") if isinstance(status, dict) else status,
            "details": item.get("details") or item.get("shortComment") or item.get("longComment"),
        })
    return pd.DataFrame(rows)
