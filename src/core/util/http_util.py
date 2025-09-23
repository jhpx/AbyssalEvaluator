# http_util.py

import json
from typing import Callable, TypeVar

import httpx

from src.core.util.logger import logger

T = TypeVar("T")


async def fetch_and_parse(
        client: httpx.AsyncClient,
        url: str,
        parser: Callable[[any], T | list[T]],
        data_type: str = "json",
        *,
        params=None,
        headers=None,
        auth=None):
    """
    获取并解析数据

    :param auth:
    :param params: URL参数
    :param headers: URL头
    :param client: httpx.AsyncClient 实例
    :param url: 请求的URL或本地文件路径
    :param parser: 解析函数
    :param data_type: 数据类型 ("json" 或 "text")
    :return: 解析后的数据或 None
    """
    # 根据URL协议类型决定使用哪种方式获取数据
    if url.startswith("http"):
        raw_data = await fetch_http_data(client, url, data_type=data_type, params=params, headers=headers, auth=auth)
    else:
        raw_data = fetch_local_data(url, data_type=data_type)

    if not raw_data:
        logger.error(f"无法获取数据:{url}")
        return None

    try:
        return parser(raw_data)
    except Exception as e:
        logger.error(f"解析失败: {e}")
        raise e


async def fetch_http_data(client: httpx.AsyncClient, url: str, data_type: str = "json", *, params=None, headers=None,
                          auth=None):
    """
    获取HTTP数据

    :param client: httpx.AsyncClient 实例
    :param url: 请求的URL
    :param headers: 请求头
    :param params: URL参数
    :param auth: 认证信息
    :param data_type: 数据类型 ("json" 或 "text")
    :return: 解析后的数据或原始文本
    """
    logger.info(f"使用远端网络地址: {url}")
    try:
        response = await client.get(url, params=params, headers=headers, auth=auth, timeout=100)
        response.raise_for_status()
        logger.info(f"请求成功")

        if data_type == "json":
            return response.json()
        else:  # text/csv
            return response.text
    except httpx.HTTPError as e:
        logger.error(f"请求失败: {url} - 错误: {e}")
        return {} if data_type == "json" else ""


def fetch_local_data(file_path: str, data_type: str = "json"):
    """
    获取本地数据

    :param file_path: 本地文件路径
    :param data_type: 数据类型 ("json" 或 "text")
    :return: 解析后的数据或原始文本
    """
    logger.info(f"使用本地文件地址: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            logger.info(f"打开成功")
            if data_type == "json":
                return json.load(f)
            else:  # text/csv
                return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"无法解析 JSON 文件: {file_path}")
