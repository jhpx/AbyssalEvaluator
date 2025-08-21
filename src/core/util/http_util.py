# http_util.py

import json
from typing import Dict, Callable, List, TypeVar

import httpx

from src.core.util.logger import logger

T = TypeVar("T")


async def fetch_and_parse(
        client: httpx.AsyncClient,
        url: str,
        parser: Callable[[dict], T | List[T]],
        *,
        headers: Dict = None,
        params: Dict = None, ):
    """
    获取并解析数据

    :param params: URL参数
    :param headers: URL头
    :param client: httpx.AsyncClient 实例
    :param url: 请求的URL或本地文件路径
    :param parser: 解析函数
    :return: 解析后的数据或 None
    """
    # 根据URL协议类型决定使用哪种方式获取数据
    if url.startswith("http"):
        raw_data = await fetch_http_json(client, url, headers, params)
    else:
        raw_data = await fetch_local_json(url)

    if not raw_data:
        logger.error(f"无法获取数据:{url}")
        return None

    try:
        return parser(raw_data)
    except Exception as e:
        logger.error(f"解析失败: {e}")
        raise e


async def fetch_http_json(client: httpx.AsyncClient, url: str, headers=None, params=None) -> Dict:
    logger.info(f"使用远端网络地址: {url}")
    try:
        response = await client.get(url, headers=headers, params=params, timeout=100)
        response.raise_for_status()
        logger.info(f"请求成功: {url}")
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"请求失败: {url} - 错误: {e}")
        return {}


async def fetch_local_json(file_path: str) -> Dict:
    logger.info(f"使用本地文件地址: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON 文件未找到: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析 JSON 文件: {file_path}")

