# src/utils/logger.py
import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

# 创建 logs 目录（如果不存在）
os.makedirs("logs", exist_ok=True)

# 获取根 logger
logger = logging.getLogger("AbyssalEvaluator")
logger.setLevel(logging.DEBUG)  # 设置全局最低日志级别

# 移除已有的 handler，防止重复添加
logger.handlers.clear()

# 控制台 handler（带颜色输出建议配合 colorlog）
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# 按每天轮转日志文件
file_handler = TimedRotatingFileHandler(
    "logs/app.log",
    when="midnight",  # 每天凌晨切换
    backupCount=7,  # 保留最近 7 天的日志
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

__all__ = ["logger"]
