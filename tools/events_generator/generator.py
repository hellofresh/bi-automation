"""Events Generator

Usage:
    generator.py run [--number=<ne>] [--message=<kn>] [--routing-key=<kn>] [--rabbit-host=<kn>] [--exchange=<kn>]
    generator.py -h | --help

Options:
    --number=<ne>       Number of events to send to RabbitMQ [default: 10].
    --message=<kn>      String with the json payload
    --routing-key=<kn>  To which routing key send the message
    --rabbit-host=<kn>  To which host connect to RabbitMQ
    --exchange=<kn>     To which exchange to connect
    -h --help           Show this screen.
    --version           Show version
"""
import os

from docopt import docopt
from rabbitmq import RabbitMQProducer


class EventGenerator(object):
    def __init__(self, rabbit_mq_url, exchange, routing_key):
        self.routing_key = routing_key
        self.exchange = exchange
        self.rabbit_mq_url = rabbit_mq_url

    def send_events(self, number, payload):
        self.__validate_input(number)

        rabbit_connexion = RabbitMQProducer(self.rabbit_mq_url)
        rabbit_connexion.connect()

        for i in xrange(0, number):
            print '[{}] Sending event'.format(str(i))

            rabbit_connexion.send(
                payload,
                self.exchange,
                self.routing_key
            )

        rabbit_connexion.connection.close()

    def __validate_input(self, number):
        if not isinstance(number, int):
            raise Exception('Number should be an integer')
        if number <= 0:
            raise Exception('Number should be bigger than 0')


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Events generator v1.1')

    number_of_events = int(arguments.get('--number'))
    exchange = arguments.get('--exchange')
    routing_key = arguments.get('--routing-key')
    host = arguments.get('--rabbit-host')
    message = arguments.get('--message')

    event_generator = EventGenerator(
        host, exchange, routing_key
    )

    event_generator.send_events(number_of_events, message)
