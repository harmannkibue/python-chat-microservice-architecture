import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://auoxxhit:igbX7XJhQa_Wgcf8pfzvx1P4JJ5UKQuW@beaver.rmq.cloudamqp.com/auoxxhit')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    body = json.loads(body)
    print("Received the message>>>><<<<", body)
    product = Product.objects.get(id=body)
    product.likes += 1
    product.save()


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("HElllo started consuming in the admin>>>>>>>><<<<<<<")

channel.start_consuming()

channel.close()
