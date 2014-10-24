'''
Monitoring Runner
'''

# Import python libs
import logging
import os.path
import time

# Import salt libs
import salt.payload


db = '/var/lib/salt/master/monitoring.db/'
log = logging.getLogger(__name__)


def process_checks(minion_id, data):

    # Update the cache
    serial = salt.payload.Serial('msgpack')
    with open(os.path.join(db, minion_id), 'w') as fn:
        serial.dump({'time': time.time(), 'results': data}, fn)

    for check, v in data.items():
        for name, results in v.items():
            if results['status']['failure'] is True:
                # alerting goes here
                log.warning(results)
