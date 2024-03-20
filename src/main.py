import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json


from .config.settings import settings
from .graphql.schema import Query

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/annotations")
def read_annotations():

    with open('./data/anno_tree.json') as f1:
        data = json.load(f1)

        with open('./data/annotation_mapping.json') as f2:
            mapping = json.load(f2)

            anno_tree = []

            for elt in data:
                if elt['leaf'] == True:
                    try:
                        elt['api_field'] = mapping[elt['name']]
                        anno_tree.append(elt)
                    except KeyError:
                        pass
                else:
                    anno_tree.append(elt)

            return {"results": anno_tree}


if __name__ == "__main__":
    print(f'Debug...{settings.DEBUG}')
    print(f'Starting server...{settings.FASTAPI_PORT}')
    # uvicorn.run("main:app", host=settings.ES_HOST, port=settings.FASTAPI_PORT, reload=settings.DEBUG, log_level='info', log_config='./log.ini')
    uvicorn.run("main:app", host=settings.ES_HOST, port=settings.FASTAPI_PORT, reload=settings.DEBUG)