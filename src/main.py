from faststream import FastStream

from presentation.message_queue.handlers.broker import broker

app = FastStream(broker)
