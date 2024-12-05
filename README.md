This is a FastAPI project which uses strawberry to query an elasticsearch database.  

### Live API
This API is live at - http://annoq.org/api-v2/

## API Endpoints
 1. **/graphql** - Graphql endpoint of the API where all the queries can be made through strawberry graphiQL.
 2. **/annotations** - Returns a json with the annotation tree which has field names for strawberry queries.
 3. **/download/{folder}/{name}** - Downloads a text file using the download path returned in the download graphql query.  

# Installations 
Before you begin, make sure you have the following installed:
1. Python: Install Python 3.9 or later. You can download it from [python.org](https://www.python.org/downloads/). 
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

Annoq has 500+ attributes, so the strawberry type for it had to be generated dynamically as it would not make sense to manually write 500 fields. This class has to be executed whenever where are any changes in the schema:

First a json schema was generated which takes the mapping for the elasticsearch database and creates a schema for a pydantic Baseclass. 
After this scripts/class_generators/class_schema.json was generated. The python file of the pydantic Baseclass - models/Snps.py is generated using datamodel-codegen.

All of this can be done using the bash script and running the following command - 

```bash
scripts/class_generators/generate_model.sh
```

Make sure that the above scripts has permissions, if not run 

```bash
chmod +x scripts/class_generators/generate_model.sh
```

## Cron job setup 
Change the cron_job.sh file change downloads in line 1 to the absolute path of the download folder in this repo after cloning and then run the following command which clears the download folder once a week at midnight.  
```
chmod +x cron_job.sh
./cron_job.sh
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