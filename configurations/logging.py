import sys
from uuid import UUID

from loguru import logger

from ..models.enums import LogLevelEnum


def logger_init(log_level: LogLevelEnum, default_uuid: str | None = None) -> None:
    logger.remove()
    default_uuid = default_uuid or str(UUID(int=0))
    m_format: str = "{time:HH:mm:ss:ms} | {level} | {name} | {extra[uuid]} | <level>{message}</level>"
    logger.add(sys.stdout, colorize=True, format=m_format, level=log_level)
    logger.configure(extra={"uuid": default_uuid, "key_id": "anonymous"})
