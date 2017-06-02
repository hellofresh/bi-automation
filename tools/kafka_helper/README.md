## Kafka Consumer/Producer

Some times we need to check the whole flow from Kafka to Flume it's working 
properly. To simplify this process you can use these two scripts to:

### Consume Events

With the `consumer.py` script you can receive all the messages sent to a 
specific topic/s in any environmnet, like staging or production.

You can use this script as follows:

`python consumer.py --servers=kafka000.staging.bi.hellofresh.io:9092,kafka001.staging.bi.hellofresh.io:9092 --topics=boxes_shipped_status`

This will listen to production for all the events sent to the topic 
`boxes_shipped_status`, you can listen to more than one topic separating each one 
by a comma.

### Produce Events

When we create a new configuration in Flume we have to wait until we start 
receiving events to Kafka to know if the Flume configuration it's working.

With this produce script we can send events as follows:

`python producer.py --servers=kafka000.staging.bi.hellofresh.io:9092,kafka001.staging.bi.hellofresh.io:9092 --topic=boxes_shipped_status --message="{'message': 'json'}"`
