__author__ = 'agerasym'


class Borg(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.__dict__ = cls._shared_state
        return obj