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

Each SNP has over 800+ attributes, hence the strawberry type was generated dynamically. This class has to be executed whenever where are any changes to the schema:

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


# To run the project

```bash
python -m src.main
```

# Testing
To run the tests on the code use the following command
```
python -m pytest test
```