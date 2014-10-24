# Import python libs
import logging

# Import salt libs
import salt.payload

# Import third party libs


db = '/var/lib/salt/minion/monitoring.db'
log = logging.getLogger(__name__)


__virtualname__ = 'monitoring'


def __virtual__():
    return __virtualname__


def returner(ret):
    serial = salt.payload.Serial('msgpack')
    try:
        with open(db) as fn:
            cache = serial.load(fn)
    except IOError:
        cache = {}

    event_data = {}
    cache_data = {}
    minion_id = ret['id']

    for _, result in ret['return'].items():
        data = result['data']
        log.warning(data)
        check = data['check']
        name = data['name']
        del data['check']
        del data['name']

        previous = cache.get(check, {}).get(name)
        status = data.get('status')
        data['status'] = {'current': status,
                          'previous': previous,
                          'changed': previous != status,
                          'failure': (not result['result'])}
        log.warning(data['status'])
        
        if check not in event_data:
            event_data[check] = {}
        if check not in cache_data:
            cache_data[check] = {}

        event_data[check][name] = data
        cache_data[check][name] = status

    with open(db, 'w') as fn:
        serial.dump(cache_data, fn)

    __salt__['event.fire_master'](event_data, 'salt/monitor/' + minion_id)
