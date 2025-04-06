from faststream import FastStream

from presentation.message_queue.handlers.report import broker

app = FastStream(broker)
