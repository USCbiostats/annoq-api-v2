from fastapi.responses import FileResponse

import strawberry
from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from fastapi.middleware.cors import CORSMiddleware
from strawberry.extensions import MaskErrors
from src.data_adapter.snp_attributes import get_snp_attrib_json
import uvicorn
import multiprocessing

import json


from src.config.settings import settings
from src.graphql.schema import Query
from src.graphql.annoq_api_schema import AnnoqApiQuery

from src.utils import clean_field_name

from src.routers import (
    snp)

site_app = FastAPI()
api_app = FastAPI()

origins = ["*"]

site_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False), extensions=[MaskErrors()])
graphql_router = GraphQLRouter(schema)
site_app.include_router(graphql_router, prefix="/graphql")

# public_schema = strawberry.Schema(query=AnnoqApiQuery, config=StrawberryConfig(auto_camel_case=False), extensions=[MaskErrors()])
# public_app = GraphQLRouter(public_schema, graphql_ide="apollo-sandbox")
# app.include_router(public_app, prefix="/openApi")




@site_app.get("/")
def read_root():
    return {"Annoq GraphQL API version": "V2"}


@site_app.get("/annotations")
def read_annotations():
    """
    Endpoint to get annotation tree with API field names

    Returns: Annotation tree with API field names
    """

    with open('./data/anno_tree.json') as f:
        data = json.load(f)
        anno_tree = []

        for elt in data:
            if elt['leaf'] == True:
                try:
                    name = clean_field_name(elt['name'])
                    elt['api_field'] = name
                    anno_tree.append(elt)
                except KeyError:
                    pass
            else:
                anno_tree.append(elt)

        return {"results": anno_tree}
    
@site_app.get("/download/{folder}/{name}")
async def download_file(folder: str, name: str):
    """
    Endpoint for downloading files

    Returns: Downloaded File Response
    """
    if folder not in settings.SITE_DOWNLOAD_DIR:
        raise HTTPException(status_code=400, detail="Invalid folder")
    return FileResponse(path=f"{folder}/{name}", filename=name, media_type='application/octet-stream')





api_app.include_router(snp.router)

@api_app.get("/")
def read_root():
    return {"Annoq API version": "V2"}


@api_app.get("/snpAttributes")
def read_snp_attributes():
    return get_snp_attrib_json()

def run_site_app():
    print(f'Debug...{settings.DEBUG}')
    print(f'Starting site server.  ..{settings.SITE_PORT}')
    # uvicorn.run("main:site_app", host=settings.ES_HOST, port=settings.SITE_PORT, reload=settings.DEBUG, log_level='info', log_config='./log.ini')
    uvicorn.run("src.main:site_app", host=settings.SITE_HOST, port=settings.SITE_PORT, reload=True)
    
    
def run_api_app():    
    print(f'Debug...{settings.DEBUG}')
    print(f'Starting api server.  ..{settings.API_PORT}')    
    uvicorn.run("src.main:api_app", host=settings.API_HOST, port=settings.API_PORT, reload=True)           




if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_site_app)
    p2 = multiprocessing.Process(target=run_api_app)
    p1.start()
    p2.start()
    p1.join()
    p2.join()



# if __name__ == "__main__":
#     print(f'Debug...{settings.DEBUG}')
#     print(f'Starting site server.  ..{settings.SITE_PORT}')
#     # uvicorn.run("main:site_app", host=settings.ES_HOST, port=settings.SITE_PORT, reload=settings.DEBUG, log_level='info', log_config='./log.ini')
#     uvicorn.run("src.main:site_app", host=settings.SITE_HOST, port=settings.SITE_PORT, reload=True)
#     print(f'Starting api server.  ..{settings.API_PORT}')    
#     uvicorn.run("src.main:api_app", host=settings.API_HOST, port=settings.API_PORT, reload=True)    