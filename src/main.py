from dishka import make_async_container
from dishka.integrations.faststream import (
    FastStreamProvider,
    setup_dishka,
)
from faststream import FastStream
from faststream.redis import RedisBroker

from bootstrap.config import Config, load_config_from_file
from presentation.message_queue import handlers


def create_app() -> FastStream:
    config = load_config_from_file()
    broker = RedisBroker(config.message_queue_url)
    app = FastStream(broker)
    container = make_async_container(
        FastStreamProvider(),
        context={Config: config},
    )
    setup_dishka(container=container, app=app, auto_inject=True)
    broker.include_routers(
        handlers.all_chats_report.router,
        handlers.report.router,
    )
    return app
