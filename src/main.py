from fastapi.responses import FileResponse
import strawberry
from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from fastapi.middleware.cors import CORSMiddleware
from strawberry.extensions import MaskErrors
import uvicorn
import json


from src.config.settings import settings
from src.graphql.schema import Query
from src.utils import clean_field_name

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False), extensions=[MaskErrors()])
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"Annoq API version": "V2"}


@app.get("/annotations")
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
    
@app.get("/download/{folder}/{name}")
async def download_file(folder: str, name: str):
    """
    Endpoint for downloading files

    Returns: Downloaded File Response
    """
    if folder not in settings.DOWNLOAD_DIR:
        raise HTTPException(status_code=400, detail="Invalid folder")
    return FileResponse(path=f"{folder}/{name}", filename=name, media_type='application/octet-stream')


if __name__ == "__main__":
    print(f'Debug...{settings.DEBUG}')
    print(f'Starting server.  ..{settings.FASTAPI_PORT}')
    # uvicorn.run("main:app", host=settings.ES_HOST, port=settings.FASTAPI_PORT, reload=settings.DEBUG, log_level='info', log_config='./log.ini')
    uvicorn.run("src.main:app", host=settings.ES_HOST, port=settings.FASTAPI_PORT, reload=settings.DEBUG)