from kennyg.decorator import CaptureListItem, CaptureKeyValue, BaseDecorator

__author__ = 'brent'


class KeyValueCollector(dict):
    def __init__(self, *args, **kw):
        super(KeyValueCollector,self).__init__(*args, **kw)
        self.collection = {}
        for key, value in self.iteritems():
            dict.__setitem__(self, key, self._decorator(value))

    def _decorator(self, value):
        if type(value) == KeyValue:
            value = CaptureKeyValue(value, dictionary_callback=lambda: self.collection)
        return value

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, self._decorator(value))

    def start(self, *args, **kwargs):
        self.collection = {}

    def value(self, *args, **kwargs):
        return self.collection


class ValueCollector(dict):
    def __init__(self, *args, **kw):
        super(ValueCollector,self).__init__(*args, **kw)
        self.collection = []
        for key, value in self.iteritems():
            dict.__setitem__(self, key, self._decorator(value))

    def _decorator(self, value):
        if hasattr(value, 'value'):
            value = CaptureListItem(value, list_callback=lambda: self.collection)
        return value

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, self._decorator(value))

    def start(self, *args, **kwargs):
        self.collection = []

    def value(self, *args, **kwargs):
        return self.collection


class Value(object):
    """
    Returns the value provided for an element
    """
    def value(self, value):
        return value


class KeyValue(BaseDecorator):
    """
    Returns a key-value pair for an elements value, where the key is set during initialization
    """
    def __init__(self, key, obj=None, *args, **kwargs):
        self.obj = obj if obj is not None else Value()
        super(KeyValue, self).__init__(self.obj, *args, **kwargs)
        self.key = key

    def value(self, value):
        value = self.obj.value(value)
        return {self.key: value}


