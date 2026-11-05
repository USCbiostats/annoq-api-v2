This is a FastAPI project which uses strawberry to query an elasticsearch database.  

### Live API
This API is live at - https://api-v2.annoq.org/docs.


# Installation 
Before you begin, make sure you have the following installed:
1. Python: Install Python 3.11 or later. You can download it from [python.org](https://www.python.org/downloads/).
 ```bash
pyenv install 3.11.9
pyenv local 3.11.9
```
2. Docker Desktop: Install Docker Desktop. You can download it from [docker-desktop](https://www.docker.com/products/docker-desktop/).

# Project Setup
1. Clone this repository.

```bash
git clone https://github.com/USCbiostats/annoq-api-v2.git
cd annoq-api-v2
```

1. Create a python virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

1. Install the dependencies

```bash
pip install -r requirements.txt
```

1. Create your `.env` from the sample for the stack you serve, then edit it (see [Configuration](#configuration-env)).
This branch carries the TOPMed annotation tree, so use the TOPMed sample:

```bash
cp .env.topmed .env   # TOPMed (topmed.annoq.org)
```

1. Start Elasticsearch. **This repo has no `docker-compose` file** — all database containers live
in [annoq-database](https://github.com/USCbiostats/annoq-database). With Docker Desktop running:

```bash
cd ../annoq-database && docker-compose up -d
```

Elasticsearch comes up on http://localhost:9200 and Kibana on http://localhost:5601. Wait for
`curl localhost:9200/_cluster/health` to leave `red` (shard recovery takes a minute), then make sure
this repo's `.env` (`ES_URL`, `ES_INDEX`) points at that instance and index.

1. Run the API **from this repo's root** — the code opens `./data/anno_tree.json` by relative path,
so the working directory matters:

```bash
uvicorn src.main:app --reload --port 8001
```

The API is then on http://localhost:8001 (`/docs` for REST, `/graphql` for the playground).

## Configuration (.env)

The API reads its settings from `.env` in the project root when it starts
(`src/config/settings.py`). `.env` is ignored by git, so each deployment keeps its own. Start from
the sample that matches the Elasticsearch index you serve:

| Sample | Stack | `ES_INDEX` | Genome build | dbSNP release | WGSA version |
| --- | --- | --- | --- | --- | --- |
| `.env.hrc` | HRC r1.1 (annoq.org) | `annoq-annotations-v5` | GRCh37/hg19 | 151 | 0.8 (probable) |
| `.env.topmed` | TOPMed Freeze 8 (topmed.annoq.org) | `annoq-annotations-tm-20260828` | GRCh38/hg38 | 155 | 0.95 |

`.env-example` is the generic template. On this TOPMed branch it describes TOPMed data
(`DATA_RSID_COL = "rs_dbSNP"`, GRCh38/hg38, dbSNP 155, WGSA 0.95); on `master` it describes HRC.

1. Copy the sample to `.env`. Copying replaces the whole file, so back up an existing `.env`
   first if it holds real secrets:

    ```bash
    cp .env .env.bak        # only if you already have a .env
    cp .env.hrc .env        # or: cp .env.topmed .env
    ```

2. Edit `.env` as necessary:
    - `GA_API_SECRET`: the samples hold a placeholder; set the real Google Analytics secret.
    - `ES_HOST`, `ES_PORT`, `ES_URL`: point these at your Elasticsearch if it is not
      `localhost:9200`.
    - `ES_INDEX`: change it if your index has a different name (for example a newer TOPMed load).
    - `SITE_HOST`, `SITE_PORT`, `SITE_URL`: where the API listens. The samples use 8000 for HRC and
      8001 for TOPMed so both can run side by side.
    - `ANNOQ_GENOME_BUILD`, `ANNOQ_DBSNP_RELEASE`, `ANNOQ_WGSA_VERSION`: describe the data in
      `ES_INDEX`. Keep them in step with the index; change them only when the index is rebuilt from
      different data.

3. Restart the API so it rereads `.env`.

To switch stacks later, repeat step 1 with the other sample and redo step 2.

Copying `.env` does not switch the annotation tree. `/annotations` and the data version in
`/version` come from `data/anno_tree.json`, which in this branch is the TOPMed tree (`chr` version
`TOPMed: Freeze 8`). The HRC tree (`chr` version `HRC.r1-1`) is on `master`, so serve HRC from a
checkout of `master` and TOPMed from a checkout of this branch.

### Version information

`GET /version` describes the data this deployment serves. AnnoQ clients (annoq-site-v2, SNPWay)
read it instead of hardcoding these values. On this TOPMed branch (with `.env.topmed`):

```json
{
  "api_version": "2.5",
  "data_version": "TOPMed: Freeze 8",
  "genome_build": "GRCh38/hg38",
  "dbsnp_release": "155",
  "wgsa_version": "0.95"
}
```

(The HRC deployment on `master` returns `HRC.r1-1`, `GRCh37/hg19`, `151`, `0.8`.)

`data_version` is the version of the `chr` field in `data/anno_tree.json`. `genome_build`,
`dbsnp_release` and `wgsa_version` come from `ANNOQ_GENOME_BUILD`, `ANNOQ_DBSNP_RELEASE` and
`ANNOQ_WGSA_VERSION` in `.env`, and are `null` when `.env` leaves them out.

## Sample Elasticsearch Data Setup

Follow the https://github.com/USCbiostats/annoq-database repository and use the sample_data folder to setup the sample data for elasticsearch.  If necessary, modify `ES_URL` and `ES_INDEX` in `.env` to reflect the database (see [Configuration](#configuration-env)). 


### Dynamic Snps class generation

Each SNP has 800+ attributes, so the Strawberry type is generated rather than hand-written.
Regenerate whenever the Elasticsearch schema changes — new/removed columns, or changed labels in
`data/anno_tree.json` / `data/api_mapping_anno_tree.json`.

> **Run `scripts/class_generators/generate_model.sh`. Do not run the generator on its own.**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

chmod +x scripts/class_generators/generate_model.sh   # first time only
scripts/class_generators/generate_model.sh
```

#### Why the script, and not `python3 -m scripts.class_generators.generator`

Generation is **two steps**, and the generator is only the first:

| Step | Command | Produces |
|---|---|---|
| 1 | `python3 -m scripts.class_generators.generator` | `scripts/class_generators/generated_schemas/snp_schema.json`, `snp_aggs_schema.json` |
| 2 | `datamodel-codegen` (×2) + post-processing `sed`s | `src/graphql/models/generated/snp.py`, `snp_aggs.py` |

`generate_model.sh` runs both. Running only step 1 rewrites the JSON schemas and leaves the
pydantic models untouched — so the API keeps serving the **old** field set with no error and no
warning. The give-away is a timestamp mismatch:

```bash
ls -la scripts/class_generators/generated_schemas/*.json src/graphql/models/generated/*.py
```

If the `.json` files are newer than the `.py` files, step 2 did not run.

#### Prerequisites and follow-up

- **The generator reads the LIVE Elasticsearch mapping**, not a file. Point `ES_URL` / `ES_INDEX`
  in `.env` at an index that already contains the fields you want exposed. A field must exist in
  the index before the API can expose it.
- **Restart the API afterwards** (`python -m src.main`) — the models are imported at start-up, so a
  running server keeps serving the previous types.
- The generated files are **gitignored build artifacts**. Never commit
  `src/graphql/models/generated/` or `scripts/class_generators/generated_schemas/`.

#### Verifying the regeneration

Check that a field you expect actually landed, and that a removed one is gone:

```bash
grep -c "^    chr_pos:" src/graphql/models/generated/snp.py     # expect 1
grep -c "HRC_rs_dbSNP151" src/graphql/models/generated/snp.py   # expect 0
```

Or query the running API's schema directly:

```bash
curl -s http://localhost:8001/graphql -H 'Content-Type: application/json' \
  -d '{"query":"{__type(name:\"Snp\"){fields{name}}}"}' | grep -c chr_pos
```

#### Downstream: the stage-4 sites

**Stage 4 is split by stack:** **annoq-site-v2** (React + Vite) serves **annoq.org (HRC r1.1)**, and
**annoq-site** (Angular 9) serves **topmed.annoq.org (TOPMed Freeze 8)**. Both generate TypeScript
types from a GraphQL endpoint that defaults to the **deployed** API, so both may need regenerating
after a schema change here.

- **annoq-site** — endpoint set in `graphql_codegen.ts`.
- **annoq-site-v2** — endpoint from `src/lib/environment.ts` (`annotationApiV2`), overridable per
  command with `VITE_ANNOQ_API_V2=... npm run graphql_codegen`. Its generated
  `src/generated/graphql.ts` is read by the build's typecheck, so **codegen must precede
  `npm run build`**.

To pick up API changes that are not yet deployed, point that endpoint at your local server
(`http://localhost:<SITE_PORT>/graphql` — `SITE_PORT` comes from your env; the Docker image
defaults to `8000`) before running `npm run graphql_codegen` — otherwise codegen succeeds against
the deployed schema and the site fails to compile against arguments and fields your local API has
but production does not.

# To run the project

```bash
python -m src.main
```

# Testing
To run the tests on the code use the following command
```
python -m pytest test
```