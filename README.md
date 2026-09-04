# NFL Player Prop v0.3.0a4 Slate-Specific Handoff Patch

Adds `--aita-event-id` (repeatable) and `--slate-label` to `nfl-model run` so each late-phase production run can create one immutable handoff ZIP for a specific betting window rather than all Week-1 games.

Validated against the v0.3.0a3 codebase: 27 tests passed and slate-subset helper test passed.
