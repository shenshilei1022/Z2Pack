#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    08.03.2016 10:21:06 CET
# File:    _helpers.py

"""Coding tools, not related to the 'physical/computation logic' of Z2Pack."""

import os
import json
import tempfile
import contextlib

from fsc.export import export

from . import _encoding

__all__ = ['serializer']

class _Proxy:
    """A simple proxy type"""
    def __init__(self, initval=None):
        self.val = initval
        
    def set(self, val):
        self.val = val

    def __getattr__(self, key):
        return getattr(self.val, key)

serializer = _Proxy(json)

def _check_binary():
    return serializer.__name__ in ['pickle', 'msgpack']

def save_result(result, file_path):
    """Pickles result in an atomic way by first creating a temporary file and then moving to the file_path."""
    with tempfile.NamedTemporaryFile(
        delete=False,
        mode='wb' if _check_binary() else 'w'
    ) as f:
        # First try msgpack / json interface
        try:
            serializer.dump(result, f, default=_encoding.encode)
        # then try pickle interface
        except TypeError:
            serializer.dump(result, f)
        os.replace(f.name, file_path)

@export
def load_result(path):
    with open(path, 'rb' if _check_binary() else 'r') as f:
        # First try msgpack / json interface
        try:
            return serializer.load(f, object_hook=_encoding.decode)
        # then try pickle interface
        except TypeError:
            return serializer.load(f)
