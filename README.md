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

1. Make sure that the Docker Desktop is running. Build the Docker image and start the container.

```bash
docker-compose up --build
```

1. Once the image and containers are made, the containers can be started from Docker Desktop or using the following command 

```bash
docker-compose up
```

The fastAPI application would be running on http://0.0.0.0:8000 and the elasticsearch instance would be on http://0.0.0.0:9200

## Sample Elasticsearch Data Setup

Follow the https://github.com/USCbiostats/annoq-database repository and use the sample_data folder to setup the sample data for elasticsearch.  If necessary, modify file .env to reflect URL of database. 


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

#### Downstream: annoq-site

`annoq-site` generates its TypeScript types from a GraphQL endpoint set in its `graphql_codegen.ts`,
which defaults to the **deployed** API. To pick up API changes that are not yet deployed, point that
`schema:` at your local server (e.g. `http://localhost:8001/graphql`) before running
`npm run graphql_codegen` — otherwise codegen succeeds against the deployed schema and the site
fails to compile against arguments and fields your local API has but production does not.


# To run the project

```bash
python -m src.main
```

# Testing
To run the tests on the code use the following command
```
python -m pytest test
```