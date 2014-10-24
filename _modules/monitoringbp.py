# -*- coding: utf-8 -*-
'''
Backported functions

'''

# Import python libs
import re
import logging

# Import salt libs
from salt._compat import string_types


log = logging.getLogger(__name__)


non_decimal = re.compile(r'[^\d.]+')


def check_thresholds(value, rules):
    for rule in rules:
        params = rule.values()[0] or {}
        label = rule.keys()[0]
        minimum = params.get('minimum')
        maximum = params.get('maximum')
        result = params.get('result', False)

        if minimum:
            if isinstance(minimum, string_types):
                minimum = non_decimal.sub('', minimum)
            try:
                minimum = float(minimum)
            except ValueError, TypeError:
                raise TypeError('"minimum" must be a number')

        if maximum:
            if isinstance(maximum, string_types):
                maximum = non_decimal.sub('', maximum)
            try:
                maximum = float(maximum)
            except ValueError, TypeError:
                raise TypeError('"maximum" must be a number')

        if minimum and maximum:
            if minimum >= maximum:
                raise ValueError('minimum must be less than maximum')

        if not minimum and not maximum:
            return (label, None, None, result)
            raise ValueError('at least one of minimum or maximum must be '
                             'provided for every rule')

        if minimum and value < minimum:
            return (label, 'low', minimum, result)
        if maximum and value > maximum:
            return (label, 'high', maximum, result)
    return ('other', None, None, False)
