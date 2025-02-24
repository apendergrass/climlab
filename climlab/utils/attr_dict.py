from collections import OrderedDict


class AttrDict(dict):
    '''
    Constructs a dict object with attribute access to data.
    '''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class OrderedAttrDict(OrderedDict):
    '''
    Constructs an collections.OrderedDict object with attribute access to data.
    '''
    def __init__(self, *args, **kwargs):
        super(OrderedAttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
