#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by lingjiao.lc

"""
Note, in my script, a tab equals four blanks.
You must have a check of your indentation.
"""

import os
import sys

class EosException(Exception):
    message = 'An unknown exception'

    def __init__(self, msg=None, **kwargs):
        self.kwargs = kwargs
        if msg is None:
            msg = self.message

        try:
            msg = msg % kwargs
        except Exception:
            msg = self.message

        super(EosException, self).__init__(msg)


class mapFull(Exception):
    message = "Map is full"
    def __init__(self, msg=None):
        super(mapFull, self).__init__(msg)

if __name__ == "__main__":
    pass


class LvsException(Exception):
    message = 'An unknown exception occurred.'

    def __init__(self, code=0, message=None, **kwargs):
        self.kwargs = kwargs
        self.code = code
        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                message = self.message
        super(LvsException, self).__init__(message)