import json
import requests
import statsd

hostname = 'http://cdh-gw-notebook.live.bi.hellofresh.io:8040/v3/kafka/local/consumer'

consumers = requests.get(
    '{host}'.format(host=hostname)
)

if consumers.status_code != 200:
    print "Goodbye! I couldn't connect to Burrow"
    exit()

c = statsd.StatsClient('graphite000.tools.hellofresh.io', 8125, 'dwh.live.kafka.burrow')

payload = json.loads(consumers.content)

if payload['error'] == 'true':
    print "Error: {}".format(payload['message'])
    exit()

for consumer in payload['consumers']:
    # Now we will check the lag information
    lag_request = requests.get(
        '{host}/{consumer}/lag'.format(
            host=hostname,
            consumer=consumer
        )
    )

    if lag_request.status_code != 200:
        continue

    lag_payload = json.loads(lag_request.content)

    if lag_payload['status']['status'] != 'OK':
        continue

    c.gauge('{}.lag'.format(consumer), lag_payload['status']['totallag'])

    
