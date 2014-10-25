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
    log.info(data)
    profiles = __opts__['monitoring']['alert_profiles']['devops']
    log.info(profiles)
    # Update the cache
    serial = salt.payload.Serial('msgpack')
    with open(os.path.join(db, minion_id), 'w') as fn:
        serial.dump({'time': time.time(), 'results': data}, fn)

    for check, v in data.items():
        for name, results in v.items():
            if results['status']['failure'] is True:
                tag = '{0}/{1} ({2})'.format(minion_id, check, name)
                log.info('failure ' + tag)
                for x in profiles:
                    for service, info in x.items():
                        log.info(info)
                        tgt = info['tgt']
                        profile = info['profile']
                        log.info(profile)
                        log.info(tgt)
                        log.info(service)
                        ret = client.cmd(tgt, '{0}.trigger'.format(service),
                               [profile, tag, results['status']['current'],
                                results['message'], results['info']])
