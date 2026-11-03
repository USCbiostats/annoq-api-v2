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

```bash
cp .env.hrc .env      # HRC (annoq.org)
# or
cp .env.topmed .env   # TOPMed (topmed.annoq.org)
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

## Configuration (.env)

The API reads its settings from `.env` in the project root when it starts
(`src/config/settings.py`). `.env` is ignored by git, so each deployment keeps its own. Start from
the sample that matches the Elasticsearch index you serve:

| Sample | Stack | `ES_INDEX` | Genome build | dbSNP release | WGSA version |
| --- | --- | --- | --- | --- | --- |
| `.env.hrc` | HRC r1.1 (annoq.org) | `annoq-annotations-v5` | GRCh37/hg19 | 151 | 0.8 (probable) |
| `.env.topmed` | TOPMed Freeze 8 (topmed.annoq.org) | `annoq-annotations-tm-20260828` | GRCh38/hg38 | 155 | 0.95 |

`.env-example` is the generic template; its values match `.env.hrc`.

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
`/version` come from `data/anno_tree.json`, which in this branch is the HRC tree (`chr` version
`HRC.r1-1`). The TOPMed tree (`chr` version `TOPMed: Freeze 8`) is on the
`annoq-site-78-add-hrc-mapping-info` branch, so serve TOPMed from a checkout of that branch.

### Version information

`GET /version` describes the data this deployment serves. AnnoQ clients (annoq-site-v2, SNPWay)
read it instead of hardcoding these values:

```json
{
  "api_version": "2.5",
  "data_version": "HRC.r1-1",
  "genome_build": "GRCh37/hg19",
  "dbsnp_release": "151",
  "wgsa_version": "0.8"
}
```

`data_version` is the version of the `chr` field in `data/anno_tree.json`. `genome_build`,
`dbsnp_release` and `wgsa_version` come from `ANNOQ_GENOME_BUILD`, `ANNOQ_DBSNP_RELEASE` and
`ANNOQ_WGSA_VERSION` in `.env`, and are `null` when `.env` leaves them out.

## Sample Elasticsearch Data Setup

Follow the https://github.com/USCbiostats/annoq-database repository and use the sample_data folder to setup the sample data for elasticsearch.  If necessary, modify `ES_URL` and `ES_INDEX` in `.env` to reflect the database (see [Configuration](#configuration-env)). 


### Dynamic Snps class generation

Annoq has 500+ attributes, so the strawberry type for it had to be generated dynamically as it would not make sense to manually write 500 fields. This class has to be executed whenever where are any changes in the schema:

First json schemas were generated which takes the mapping for the elasticsearch database and creates schemas for pydantic Baseclasses. 
After scripts/class_generators/generated_schemas/snp_schema.json and scripts/class_generators/generated_schemas/snp_aggs_schema.json were generated. The python files of the pydantic Baseclasses - src/graphql/models/generated/snp.py and src/graphql/models/generated/snp_aggs.py were generated using datamodel-codegen.

If there are changes to the number of columns or labels, which would be reflected in data/anno_tree.json or data/api_mapping_anno_tree.json, the following script has to be executed to re-generate the model json file.   This will generate scripts/class_generators/generated_schemas/snp_schema.json and scripts/class_generators/generated_schemas/snp_aggs_schema.json

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m scripts.class_generators.generator
```

All of this can be done using the bash script and running the following command - 

```bash
scripts/class_generators/generate_model.sh
```

Make sure that the above scripts has permissions, if not run 

```bash
chmod +x scripts/class_generators/generate_model.sh
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