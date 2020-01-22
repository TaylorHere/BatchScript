from kafka import KafkaConsumer
consumer = KafkaConsumer()

class Consumer(object):
    self.callback = None

    def __init__(self, callback):
        self.callback = callback

    def start(self,):
        while True:
            msg = consumer.poll()
            self.callback(msg)
