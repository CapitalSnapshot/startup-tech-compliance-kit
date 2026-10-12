# Database variant: PostgreSQL

Use in prompts B4 and D1 when DB FAMILY is PostgreSQL.

## What usually breaks or needs attention

- **Version path:** target a version not older than production. Dump and restore across versions with the newer client tools. Never downgrade.
- **Extensions:** list the extensions in use and confirm each is available on the managed service and at the target version.
- **Collation and locale:** a change in the operating system's locale library between hosts can invalidate text indexes. Rebuild indexes (`REINDEX`) after moving, and record the collation of each database.
- **Roles, ownership and grants:** dump without owners (`--no-owner`) and recreate roles and grants explicitly on the target. Managed services restrict superuser actions.
- **Sequences:** confirm sequence values after the restore so inserts do not collide.
- **Large objects and special types:** check for large objects and any custom types.
- **Encoding and time zone:** confirm the database encoding (UTF8) and the server time zone.
- **Connection limits and pooling:** managed instances have lower connection ceilings; add a pooler if the app opens many connections.
- **Statistics:** run `ANALYZE` after the restore, or queries will be slow until statistics build.

## Dump and restore

```text
pg_dump -Fc <DB>  ->  pg_restore -j <N> --no-owner -d <TARGET>
```

Stream or pipe so the dump never lands on a laptop disk. For a near-zero-downtime cutover, consider logical replication from the old database to the new one and cut over once lag is zero; rehearse it first. Compare row counts and key-table checksums, run the smoke suite, and record timings in `infra/evidence/restore-timing.md`.

## Schema-only check (Phase 0)

Dump structure only (`--schema-only`), then list extensions, collations, roles, grants and any features from the list above.
