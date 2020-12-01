# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"


class DotMap(dict):
    """
    Example:
    m = DotMap({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        for arg in args:
            self._update(arg)

        self._update(kwargs)

    def _update(self, arg):
        if isinstance(arg, dict):
            for k, v in arg.items():
                v = DotMap(v) if isinstance(v, dict) else v
                self.update({k: v})
                self.__dict__.update({k: v})
        else:
            raise TypeError(f"inputs need to be  dictionary or keyword arguments")
