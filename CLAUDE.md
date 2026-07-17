# CLAUDE.md — annoq-api-v2

Standing context for Claude Code sessions in this repo. Terse; read the files it points to.

## What this repo is

**annoq-api-v2** is the **current** AnnoQ API (FastAPI + Strawberry GraphQL) — stage 3 of the
pipeline `annoq-data-builder → annoq-database → annoq-api-v2 → annoq-site`. The old `annoq-api` is
**deprecated**; do not put new work there.

- GraphQL types are **generated from the Elasticsearch schema** (`scripts/class_generators/`,
  then `datamodel-codegen`). **A field must exist in the ES index before the API can expose it.**
  Generated models live in `src/graphql/models/generated/` and are **gitignored / built at runtime**.
- ES connection + target index come from `.env` (`ES_HOST`/`ES_PORT`/`ES_URL`/`ES_INDEX`, see
  `src/config/settings.py`). Point `ES_INDEX` at a local test index to develop against it.

## Cross-repo context lives in the hub

This repo is one of several sibling repos coordinated by **`../annoq-proj`** (docs + Claude skills,
no app code). For the full platform picture — the 4-stage pipeline, the **two parallel deployment
stacks (HRC `main` / TOPMed beta)**, shared contracts, and branch/commit naming — read
`../annoq-proj/CLAUDE.md` and `../annoq-proj/docs/`. A session here does **not** auto-load the hub's
CLAUDE.md (sibling dir), so consult it explicitly when scope crosses repos.

Both deployed stacks currently serve **SNPs only (no indels)** — a property of the datasets, not the
code. api-v2 instances: `https://api-v2.annoq.org` (HRC) and `https://api-v2.topmed.annoq.org` (TOPMed).

## Active task

- **Issue #78 — add HRC-mapping search to the TOPMed dataset.** Branch
  `annoq-site-78-add-hrc-mapping-info`. See **[`docs/issue-78-hrc-mapping.md`](docs/issue-78-hrc-mapping.md)**
  for the exact change plan, ES field names, and the live local test index.

## Working rules

- Code/generated schema is the source of truth; prose docs conform to it.
- Add `pytest` coverage for resolver/query changes; verify real queries in the GraphQL playground.
- After changing the ES mapping/schema or any shared contract, regenerate types here **and** run
  `../annoq-proj` → `/annoq-doc-sync` so consumer docs (annoq-py, AnnoQR, SNPWay, site) don't drift.
