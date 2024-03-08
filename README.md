# Installations 
Before you begin, make sure you have the following installed:
1. Python: Install Python 3.9 or later. You can download it from [python.org](https://www.python.org/downloads/). 
2. Docker Desktop: Install Docker Desktop. You can download it from [docker-desktop](https://www.docker.com/products/docker-desktop/).

# Project Setup
1. Clone this repository.
```
git clone https://github.com/USCbiostats/annoq-api-v2.git
cd annoq-api-v2
```
2. Create a python virtual environment and activate it.
```
python3 -m venv venv
source venv/bin/activate
```
3. Install the dependencies
```
pip install -r requirements.txt
```
4. Make sure that the Docker Desktop is running. Build the Docker image and start the container.
```
docker-compose up --build
```
5. Once the image and containers are made, the containers can be started from Docker Desktop or using the following command 
```
docker-compose up
```
The fastAPI application would be running on http://0.0.0.0:8000 and the elasticsearch instance would be on http://0.0.0.0:9200

## Sample Elasticsearch Data Setup
Follow the https://github.com/USCbiostats/annoq-database repository and use the sample_data folder to setup the sample data for elasticsearch


### Dynamic AnnoqData class generation
Annoq has 500+ attributes, so the strawberry type for it had to be generated dynamically as it would not make sense to manually write 500 fields. Since the class is already present in this repository there is no need to run the following code again, but just for knowledge: 

First a json schema was generated using the following command which takes the mapping for the elasticsearch database and creates a schema for a pydantic Baseclass. 
```
python models/class_generation.py
```
After this models/class_schema.json was generated. The python file of the pydantic Baseclass - models/AnnoqData_class.py is generated using the following
```
datamodel-codegen --input models/class_schema.json --input-file-type jsonschema --output models/AnnoqData_class.py
```
After this manually replaced Any with Field in AnnoqData_class.py and added the following line 
```
from models.helper_models import Field
```