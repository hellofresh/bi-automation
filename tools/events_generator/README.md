## Testing the RabbitMQ -> Kandalf -> Kafka -> Flume workflow

We have a complicated set up to send events from any IT service to our DWH. 
We have to set up many configurations in different services, this can be a 
problem when we want to be sure that everything it is properly done.

That's the purpose of this service, give you a way to send a message to 
RabbitMQ to a specific Exchange and Routing Key.

You can execute the service as follows:

`python generator.py run --number=10 --message="{'test': 'test'}" --routing-key=test.events.staging --exchange=dwh --rabbit-host="http://USER:PASSWORD@common-rabbitmq000.staging.hellofresh.io:5672/%2f"`

This will send 10 messages to the `dwh` exchange and `tests.events.staging` 
routing key.