# Database variant: MySQL family (MySQL, MariaDB)

Use in prompts B4 and D1 when DB FAMILY is a MySQL-family engine.

## What usually breaks when moving to a managed service or newer version

- **SQL mode:** strict mode, `ONLY_FULL_GROUP_BY`, `NO_ZERO_DATE` and similar are often stricter on the target. Queries and inserts that worked silently now fail. Fix in application code, not by relaxing the mode.
- **Character set and collation:** legacy `latin1` or `utf8` (3-byte) tables, and default collations that differ between versions. Plan an explicit conversion to `utf8mb4` and list tables still on old collations.
- **Storage engines:** MyISAM tables do not belong on a managed service; convert to InnoDB.
- **DEFINER clauses:** views, triggers, routines and events dumped with a definer that does not exist on the target fail to load. Recreate with a valid definer or `SQL SECURITY INVOKER`.
- **Privileges:** managed services do not grant `SUPER`. Dumps that set global state may need flags removed.
- **Reserved words and syntax:** new versions add reserved words; check identifiers.
- **Table-name case sensitivity:** `lower_case_table_names` can differ; check mixed-case table names.
- **Time zone tables and defaults:** confirm the server time zone and that named time zones load.
- **Packet size and limits:** raise `max_allowed_packet` for the restore if large rows fail.
- **Version path:** target a version not older than production. Never downgrade.

## Dump and restore

```text
mysqldump --single-transaction --routines --triggers --events <DB> | <stream to target>
```

Stream over SSH directly into the scratch database; do not write the dump to a laptop disk. After the restore, compare row counts per table and checksums on key tables against the source, then run the smoke suite. Record timings in `infra/evidence/restore-timing.md`.

## Schema-only check (Phase 0)

Dump structure only (`--no-data`), then list tables by engine and collation, views and routines with definers, and any features from the list above.
