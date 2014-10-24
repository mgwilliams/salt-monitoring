# -*- coding: utf-8 -*-
'''
Disk monitoring state

Monitor the state of disk resources
'''

# Import python libs
import logging

try:
    from salt.utils.monitoring import check_thresholds
except ImportError as e:  # TODO: Get rid of this
    def check_thresholds(*args, **kwargs):
        return __salt__['monitoringbp.check_thresholds'](*args, **kwargs)


__monitor__ = [
    'status',
]


log = logging.getLogger(__name__)


def _fmt_kb(num):
    num = float(num)
    for x in ['KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%0.1f %s" % (num, x)
        num /= 1024.0


def status(name,
           maximum=None,
           minimum=None,
           thresholds=None,
           url=None):
    '''
    Return the current disk usage stats for the named mount point
    '''
    # Monitoring state, no changes will be made so no test interface needed
    ret = {'name': name,
           'result': False,
           'comment': '',
           'changes': {},
           'data': {}}

    data = {'name': name,
            'check': 'disk.status'}

    if thresholds is None:
        thresholds = [
            {'failure':
                {'minimum': minimum,
                 'maximum': maximum,
                 'result': False}},
        ]

    info = __salt__['disk.usage']()
    if name not in info:
        ret['result'] = False
        ret['comment'] += 'Named disk mount not present '
        return ret
    info = info[name]
    cap = int(info['capacity'].strip('%'))

    status, level, threshold, result = check_thresholds(cap, thresholds)

    if threshold:
        threshold = int(threshold)

    warning = ''
    if result is False:
        if level == 'high':
            warning = ' (above {0}% threshold)'.format(threshold)
        elif level == 'low':
            warning = ' (below {0}% threshold)'.format(threshold)

    message = ('Disk "{0}" is at {1}% '
               'capacity{2}.').format(name, cap,
                                      warning)
    ret['comment'] = '{0}: {1}'.format(status, message)

    data['message'] = message
    data['status'] = status

    if level:
        data['threshold'] = [level, threshold]

    data['info'] = {'size': _fmt_kb(info['1K-blocks']),
                    'used': _fmt_kb(info['used']),
                    'available': _fmt_kb(info['available']),
                    'capacity': info['capacity'],
                    'filesystem': info['filesystem']}

    data['metrics'] = {'size_kb': info['1K-blocks'],
                       'used_kb': info['used'],
                       'available_kb': info['available'],
                       'percent_capacity': cap}
    if url:
        data['url'] = url

    ret['data'] = data
    ret['result'] = result
    return ret
