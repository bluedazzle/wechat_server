# coding: utf-8
from __future__ import unicode_literals

import random
import string


def create_unique(count=8):
    return string.join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                      count)).replace(" ", "")
