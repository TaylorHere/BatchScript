import requests
import os
from pykafka import KafkaClient
import json
import datetime


class Consumer():

    def __init__(self, callback):
        self.client = KafkaClient(hosts="datanode01:9092,datanode02:9092,datanode03:9092")
        self.topic = client.topics['dev-syn-table-reportcontent']
        self.consumer = topic.get_simple_consumer(
            consumer_group="consumer",
            reset_offset_on_start=False
        )
        self.callback = callback

    def start(self):
        for message in consumer:
            if message is not None:
                report =str(message.value,'utf-8')
                rptjson = json.loads(report)
                self.callback(rptjson)