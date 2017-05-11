""" Kafka Producer
Usage:
    consumer.py [--servers=<kn>] [--topic=<kn>] [--message=<kn>]
    consumer.py --version
    consumer.py (-h | --help)

Options:
    -h --help       Show this screen
    --version       Show version
    --servers=<kn>  Servers separated by comma
    --topic=<kn>    Topics name
    --message=<kn>  Message string
"""
from kafka import KafkaProducer
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Kafka Producer v0.1')

    servers = None
    if arguments.has_key('--servers'):
        servers = arguments.get('--servers')

    topic = None
    if arguments.has_key('--topic'):
        topic = arguments.get('--topic')

    message = None
    if arguments.has_key('--message'):
        message = arguments.get('--message')

    producer = KafkaProducer(
        bootstrap_servers=servers
    )

    producer.send(topic, message)
