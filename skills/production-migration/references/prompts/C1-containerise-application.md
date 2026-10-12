# C1. Containerise the application

Run in: a coding agent. Phase 1, step 1.

```text
Phase 1, step 1. Create branch phase1-containers. Build: a production-grade Dockerfile using the official <RUNTIME IMAGE MATCHING PRODUCTION VERSION> base, required extensions, locked dependencies, frontend build output baked in and a non-root user; a web server container that serves every hostname in infra/inventory/host-inventory.md and proxies <ENDPOINTS TO KEEP>; a container for each side service; a cache container if the app uses one; and a compose file. Put user uploads behind a storage abstraction that can use local disk or object storage by configuration, move sessions to shared storage, add a database migration runner that records applied migrations, and fix any code that defaults to real email or live services when configuration is unset. If the application already builds a container image, reuse it and say so. Run the existing tests and open a PR. Do not merge.
```

Next: [C2. Pipeline, deploys and dev environment](C2-pipeline-deploys-dev.md)
