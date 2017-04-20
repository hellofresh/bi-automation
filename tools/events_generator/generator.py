"""Events Generator.

Usage:
    generator.py run [--number=<ne>]
    generator.py -h | --help

Options:
    --number=<ne>    Number of events to send to RabbitMQ [default: 10].
    -h --help        Show this screen.
    --version        Show version
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
    arguments = docopt(__doc__, version='Events generator v1.0')

    number_of_events = int(arguments.get('--number'))
    channel = ''
    routing_key = ''

    event_generator = EventGenerator(
        os.environ['RABBITMQ_URL'], 'dwh', 'test.events.staging'
    )

    event_generator.send_events(number_of_events, {'data': 'some_data'})
