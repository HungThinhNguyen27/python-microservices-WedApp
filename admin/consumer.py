

import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product



params = pika.URLParameters(
    'amqps://xfegjdlv:gwPdweinzsyEhylaf2nRDGYAOd2VV2pg@mustang.rmq.cloudamqp.com/xfegjdlv')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.like = product.like + 1
    product.save()
    print('Product likes increased!')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)
print('Start Consuming')
channel.start_consuming()
channel.close()
