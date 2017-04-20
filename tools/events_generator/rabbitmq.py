import pika
import json


class RabbitMQProducer(object):
    def __init__(self, url):
        self.url = url
        self.callback_function = None
        self.declared_exchanges = []
        self.connection = None
        self.channel = []

    def connect(self):
        try:
            params = pika.URLParameters(self.url)
            print self.url
            params.socket_timeout = 5

            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
        except pika.exceptions.IncompatibleProtocolError as e:
            raise Exception('Incompatible Protocol Error')
        except pika.exceptions.ConnectionClosed as e:
            raise Exception('Connection Closed')
        except Exception as e:
            raise Exception('Exception connecting {}'.format(e.message))

    def send(self, payload, exchange_topic, routing_key):
        try:
            if exchange_topic not in self.declared_exchanges:
                self.channel.exchange_declare(
                    exchange='dwh', type='topic', durable=True
                )
                self.declared_exchanges.append(exchange_topic)

            print routing_key
            self.channel.basic_publish(
                exchange='dwh',
                routing_key='test.events.staging',
                body='stuff'
            )
        except pika.exceptions.IncompatibleProtocolError as e:
            raise Exception('IncompatibleProtocol')
        except pika.exceptions.ConnectionClosed as e:
            raise Exception('ConnectionClosed')
        except Exception as e:
            print e
            exit()
            raise Exception('Error: {}'.format(e.message))

        return True
