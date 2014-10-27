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
    client = salt.client.LocalClient(__opts__['conf_file'])
    profiles = __opts__['monitoring']['alert_profiles']['devops']

    # Update the cache
    serial = salt.payload.Serial('msgpack')
    with open(os.path.join(db, minion_id), 'w') as fn:
        serial.dump({'time': time.time(), 'results': data}, fn)

    for check, v in data.items():
        for name, results in v.items():
            if results['status']['changed'] is True:
                check = '{0} ({1})'.format(check, name)
                for x in profiles:
                    for service, info in x.items():
                        profile = info['profile']
                        tgt = info['tgt']
                        ret = client.cmd(tgt, '{0}.alert'.format(service),
                                   [profile, minion_id, check,
                                   results['status']['current'],
                                   results['message'], results['info']],
                                   kwarg={'failure': results['status']['failure']})
