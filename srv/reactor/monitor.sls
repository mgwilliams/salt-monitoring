#!py
import logging


log = logging.getLogger(__name__)


def run(*args, **kwargs):
    ret = {'monitoring': {'runner.monitoring.process_checks':
        [{'minion_id': data['id']}, {'data': data['data']}]}}
    log.warning(ret)
    return ret
