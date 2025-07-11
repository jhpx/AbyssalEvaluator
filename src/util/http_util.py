import json
from typing import Dict, Callable, List, TypeVar

import httpx

from src.util.logger import logger

T = TypeVar("T")


async def fetch_and_parse(
        client: httpx.AsyncClient,
        url: str,
        parser: Callable[[dict], T|List[T]],
        use_local: bool = True,
        local_file_path: str = None):
    if use_local and local_file_path:
        raw_data = await fetch_local_json(local_file_path)
    else:
        raw_data = await fetch_http_json(client, url)

    if not raw_data:
        logger.error(f"无法获取数据:{url}")
        return None

    try:
        return parser(raw_data)
    except Exception as e:
        logger.error(f"解析失败: {e}")
        return None


async def fetch_http_json(client: httpx.AsyncClient, url: str) -> Dict:
    try:
        response = await client.get(url, timeout=100)
        response.raise_for_status()
        logger.info(f"请求成功: {url}")
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"请求失败: {url} - 错误: {e}")
        return {}


async def fetch_local_json(file_path: str) -> Dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON 文件未找到: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析 JSON 文件: {file_path}")
