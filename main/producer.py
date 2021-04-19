import pika, json

params = pika.URLParameters('amqps://auoxxhit:igbX7XJhQa_Wgcf8pfzvx1P4JJ5UKQuW@beaver.rmq.cloudamqp.com/auoxxhit')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
