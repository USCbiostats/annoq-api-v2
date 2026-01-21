from fastapi.responses import FileResponse

import strawberry
from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from fastapi.middleware.cors import CORSMiddleware
from strawberry.extensions import MaskErrors
from src.utils import field_name_mapper

import uvicorn
import json
import os
import time
from datetime import datetime, timedelta
import threading


from src.config.settings import settings
from src.graphql.schema import Query

from src.utils import clean_field_name

from src.routers import snp

# Initialize field name mappings at startup
field_name_mapper.initialize_from_anno_tree(anno_tree_path="./data/anno_tree.json")

# Create a single FastAPI app
app = FastAPI(
    title=snp.TITLE,
    summary=snp.SUMMARY,
    description=snp.DESCRIPTION,
    version=snp.VERSION,
    openapi_tags=snp.TAGS_METADATA,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up GraphQL
schema = strawberry.Schema(
    query=Query,
    config=StrawberryConfig(auto_camel_case=False),
    extensions=[MaskErrors()],
)
graphql_router = GraphQLRouter(schema)
app.include_router(graphql_router, prefix="/graphql", include_in_schema=False)

# Include REST API routes
app.include_router(snp.router)


# Add root endpoint
@app.get("/", include_in_schema=False)
def read_root():
    return {"Annoq API version": "V2"}


@app.get("/annotations", include_in_schema=False)
def read_annotations():
    """
    Endpoint to get annotation tree with API field names

    Returns: Annotation tree with API field names
    """

    if not hasattr(read_annotations, "anno_tree"):
        anno_tree = []

        with open("./data/anno_tree.json") as f:
            data = json.load(f)

            for elt in data:
                if elt["leaf"] == True:
                    try:
                        name = clean_field_name(elt["name"])
                        elt["api_field"] = name
                        anno_tree.append(elt)
                    except KeyError:
                        pass
                else:
                    anno_tree.append(elt)
        read_annotations.anno_tree = anno_tree

    return {"results": read_annotations.anno_tree}


@app.get("/download/{folder}/{name}", include_in_schema=False)
async def download_file(folder: str, name: str):
    """
    Endpoint for downloading files

    Returns: Downloaded File Response
    """
    if folder not in settings.SITE_DOWNLOAD_DIR:
        raise HTTPException(status_code=400, detail="Invalid folder")
    return FileResponse(
        path=f"{folder}/{name}", filename=name, media_type="application/octet-stream"
    )


def delete_old_files_periodically(directory, age_minutes, interval_seconds):
    def cleanup():
        while True:
            now = datetime.now()
            cutoff = now - timedelta(minutes=age_minutes)
            print(f"Deleting files at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            for filename in os.listdir(directory):
                if False == filename.endswith(".txt"):
                    continue
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if file_modified < cutoff:
                        try:
                            os.remove(filepath)
                            print(f"Deleted: {filepath}")
                        except Exception as e:
                            print(f"Error deleting {filepath}: {e}")
            time.sleep(interval_seconds)

    thread = threading.Thread(target=cleanup, daemon=True)
    thread.start()
    print(f"Started cleanup thread for '{directory}' every {interval_seconds} seconds.")


# @api_app.get("/snpAttributes")
# def read_snp_attributes():
#     return get_snp_attrib_json()


def run_app():
    delete_old_files_periodically(
        str(settings.SITE_DOWNLOAD_DIR + "/"), age_minutes=60, interval_seconds=3600
    )
    print(f"Debug...{settings.DEBUG}")
    print(f"Starting server on port {settings.SITE_PORT}")
    uvicorn.run(
        "src.main:app", host=settings.SITE_HOST, port=settings.SITE_PORT, reload=True
    )


if __name__ == "__main__":
    run_app()
