import json
from typing import Dict

import httpx

from src.util.logger import logger


async def fetch_http_json(client: httpx.AsyncClient, url: str) -> Dict:
    try:
        response = await client.get(url, timeout=100)
        response.raise_for_status()
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