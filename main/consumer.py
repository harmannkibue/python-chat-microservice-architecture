import pika, json
from main import db, Product

params = pika.URLParameters('amqps://auoxxhit:igbX7XJhQa_Wgcf8pfzvx1P4JJ5UKQuW@beaver.rmq.cloudamqp.com/auoxxhit')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received the message>>>><<<<", data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print("HElllo started consuming>>>>>>>><<<<<<<")

channel.start_consuming()

channel.close()
