import pathlib
from dataclasses import dataclass
from functools import lru_cache
from typing import Final
from zoneinfo import ZoneInfo

import tomllib

CONFIG_FILE_PATH: Final[pathlib.Path] = (
    pathlib.Path(__file__).parent.parent.parent / "config.toml"
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    message_queue_url: str
    dodo_is_api_gateway_base_url: str
    app_name: str
    api_gateway_base_url: str
    api_gateway_token: str
    timezone: ZoneInfo


@lru_cache
def load_config_from_file() -> Config:
    config = tomllib.loads(CONFIG_FILE_PATH.read_text(encoding="utf-8"))
    return Config(
        message_queue_url=config["message_queue"]["url"],
        dodo_is_api_gateway_base_url=config["dodo_is_api_gateway"]["base_url"],
        api_gateway_base_url=config["api_gateway"]["base_url"],
        api_gateway_token=config["api_gateway"]["token"],
        app_name=config["app"]["name"],
        timezone=ZoneInfo(config["app"]["timezone"]),
    )
