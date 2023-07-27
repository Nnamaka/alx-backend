#!/usr/bin/env python3
"""Basic dictionary"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """inherits from BaseCaching"""

    def __init__(self):
        """Initialize class"""
        BaseCaching.__init__(self)

    def put(self, key, item):
        """Put function"""
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        """Get function"""

        if key is not None and key in self.cache_data.keys():
            return self.cache_data[key]
        return None
