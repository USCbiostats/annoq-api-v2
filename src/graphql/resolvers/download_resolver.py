import uuid
from typing import AsyncGenerator, Any
from ...config.settings import settings


async def download_annotations_from_stream(
    fields: list[str], stream: AsyncGenerator[Any, None]
):
    """
    Download annotations from a streaming source

    Params: fields: List of fields to be returned
            stream: Async generator yielding SNP records

    Returns: string for download filename
    """
    count = 0
    filename = str(uuid.uuid4()) + ".txt"
    f = open(settings.SITE_DOWNLOAD_DIR + "/" + filename, "w")
    f.write("\t".join(fields) + "\n")

    async for doc in stream:
        count += 1
        if count > settings.SIZE_DOWNLOAD_SIZE:
            f.close()
            return "/downloads/" + filename

        li = []
        for k in fields:
            if k == "id":
                li.append(str(doc["_id"]))
            else:
                li.append(str(doc["_source"].get(k, ".")))
        f.write("\t".join(li) + "\n")

    f.close()
    return "/downloads/" + filename
