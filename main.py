import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from schema.schema import Query
from config.settings import settings

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


if __name__ == "__main__":
    print(f'Debug...{settings.DEBUG}')
    print(f'Starting server...{settings.FASTAPI_PORT}')
    # uvicorn.run("main:app", host=settings.ES_HOST, port=settings.FASTAPI_PORT, reload=settings.DEBUG, log_level='info', log_config='./log.ini')
    uvicorn.run("main:app", host=settings.ES_HOST, port=settings.FASTAPI_PORT, reload=settings.DEBUG)