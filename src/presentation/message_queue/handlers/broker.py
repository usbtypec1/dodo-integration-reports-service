from faststream.redis import RedisBroker

from bootstrap.config import load_config_from_file

broker = RedisBroker(load_config_from_file().message_queue_url)
