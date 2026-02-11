import asyncio
import hashlib
import json
import logging

import aiohttp

from src.config.settings import settings

logger = logging.getLogger(__name__)

GA4_ENDPOINT = "https://www.google-analytics.com/mp/collect"

TRACKED_PREFIXES = ("/graphql", "/docs", "/snp")


def _is_tracked_path(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in TRACKED_PREFIXES)


def _generate_client_id(client_ip: str) -> str:
    return hashlib.sha256(client_ip.encode()).hexdigest()[:16]


def _extract_graphql_operation(body: bytes) -> str:
    try:
        data = json.loads(body)
        if isinstance(data, dict):
            return data.get("operationName", "") or ""
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    return ""


async def send_ga4_event(
    path: str,
    method: str,
    client_ip: str,
    user_agent: str,
    graphql_operation: str = "",
) -> None:
    if not settings.GA_API_SECRET or not settings.GA_MEASUREMENT_ID:
        return

    params = {
        "endpoint_path": path,
        "http_method": method,
    }
    if graphql_operation:
        params["graphql_operation"] = graphql_operation
    if user_agent:
        params["user_agent"] = user_agent[:100]

    payload = {
        "client_id": _generate_client_id(client_ip),
        "events": [
            {
                "name": "api_request",
                "params": params,
            }
        ],
    }

    url = (
        f"{GA4_ENDPOINT}"
        f"?measurement_id={settings.GA_MEASUREMENT_ID}"
        f"&api_secret={settings.GA_API_SECRET}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=5)):
                pass
    except Exception as e:
        logger.debug(f"GA4 tracking error: {e}")


async def track_request(
    path: str,
    method: str,
    client_ip: str,
    user_agent: str,
    body: bytes = b"",
) -> None:
    if not _is_tracked_path(path):
        return

    graphql_operation = ""
    if path.startswith("/graphql") and method == "POST":
        graphql_operation = _extract_graphql_operation(body)

    asyncio.create_task(
        send_ga4_event(path, method, client_ip, user_agent, graphql_operation)
    )