"""Events Generator.

Usage:
    generator.py run [--number=<ne>]
    generator.py -h | --help

Options:
    --number=<ne>    Number of events to send to RabbitMQ [default: 10].
    -h --help        Show this screen.
    --version        Show version
"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Events generator v1.0')

    print arguments
