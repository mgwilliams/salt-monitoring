# -*- coding: utf-8 -*-
'''
Module for Firing Events via BigPanda.io

:configuration: This module can be used by specifying the name of a
    configuration profile in the minion config, minion pillar, or master
    config.

    For example:

    .. code-block:: yaml

        my-pagerduty-account:
            pagerduty.api_key: F3Rbyjbve43rfFWf2214
            pagerduty.subdomain: mysubdomain
'''

# Import python libs
import json
import yaml
import logging

# Import salt libs
from salt._compat import string_types

# import third party libs
import requests

log = logging.getLogger(__name__)


__virtualname__ = 'bigpanda'

def __virtual__():
    return True


def alert(profile, host, check, status, description, details, failure=True, url=None):
    api_url = 'https://api.bigpanda.io/data/v2/alerts'
    headers = {'Authorization': 'Bearer {0}'.format(profile['api_token']),
               'Content-Type': 'application/json'}

    status = profile.get('statuses', {}).get(status) or status

    if isinstance(details, string_types):
        details = yaml.safe_load(details)
        if isinstance(details, string_types):
            details = {'details': details}
    data = dict([(k, str(v)) for k, v in details.items()])

    data.update({'host': host, 'check': check, 'description': description,
                 'status': status, 'app_key': profile['app_key']})
    result = requests.request('POST', api_url, headers=headers, data=json.dumps(data), verify=False)
    return result.text
