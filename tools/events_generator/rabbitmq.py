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
                print 'creating exchange'
                self.channel.exchange_declare(
                    exchange=exchange_topic, type='topic', durable=True
                )
                self.declared_exchanges.append(exchange_topic)

            self.channel.basic_publish(
                exchange=exchange_topic,
                routing_key=routing_key,
                body=json.dumps(payload)
            )
        except pika.exceptions.IncompatibleProtocolError as e:
            return False
        except pika.exceptions.ConnectionClosed as e:
            return False
        except Exception as e:
            return False

        return True
