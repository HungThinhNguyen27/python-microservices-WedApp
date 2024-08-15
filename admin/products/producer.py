import pika
import json

params = pika.URLParameters(
    'amqps://xfegjdlv:gwPdweinzsyEhylaf2nRDGYAOd2VV2pg@mustang.rmq.cloudamqp.com/xfegjdlv')

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):

    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main',
                          body=json.dumps(body), properties=properties)
