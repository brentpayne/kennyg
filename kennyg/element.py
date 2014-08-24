from kennyg.decorator import CaptureListItem, CaptureKeyValue, BaseDecorator
from kennyg.mixin import SingletonCollectorMixIn

__author__ = 'brent'


class Collector(dict):
    """
     Abstract class that defines collector.
     Collectors wrap child elements in a Decorator Pattern to collect there
      values in a container owned by the collector.
     Subclasses must implement the _decorate function.
     It is common practice to make the collector's container accessible
      through a collection member variable or property
    """

    def __init__(self, *args, **kwargs):
        super(Collector, self).__init__(*args, **kwargs)
        for key, value in self.iteritems():
            dict.__setitem__(self, key, self._decorator(value))

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, self._decorator(value))

    def update(self, obj=None, **kwargs): # known special case of dict.update
        """
        dict.update is special cased and does not end up calling __setitem___
        overriding to ensure it gets called.
        Below is the dict.update description:
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
        In either case, this is followed by: for k in F: D[k] = F[k]
        code based on DictMixIn
        """
        if obj is None:
            pass
        elif hasattr(obj, 'iteritems'):  # iteritems saves memory and lookups
            for k, v in obj.iteritems():
                self[k] = v
        elif hasattr(obj, 'keys'):
            for k in obj.keys():
                self[k] = obj[k]
        else:
            for k, v in obj:
                self[k] = v
        if kwargs:
            self.update(kwargs)

    def _decorator(self, value):
        """
        function used to apply a CollectorDecoratorPattern to all values added to the dictionary
        """
        raise NotImplemented()


class ValueCollector(Collector):
    def __init__(self, *args, **kw):
        super(ValueCollector,self).__init__(*args, **kw)
        self.collection = []

    def _decorator(self, value):
        if hasattr(value, 'value'):
            value = CaptureListItem(value, list_callback=lambda: self.collection)
        return value

    def start(self, *args, **kwargs):
        self.collection = []

    def value(self, *args, **kwargs):
        return self.collection


class ListCollector(Collector):
    def __init__(self, *args, **kw):
        super(ValueCollector,self).__init__(*args, **kw)
        self.collection = []

    def _decorator(self, value):
        if hasattr(value, 'value'):
            value = CaptureListItem(value, list_callback=lambda: self.collection)
        return value

    def start(self, *args, **kwargs):
        self.collection = []

    def value(self, *args, **kwargs):
        return self.collection


class KeyValueCollector(Collector):
    def __init__(self, *args, **kw):
        super(KeyValueCollector,self).__init__(*args, **kw)
        self.collection = {}

    def _decorator(self, value):
        if type(value) in (KeyValue, dict):
            value = CaptureKeyValue(value, dictionary_callback=lambda: self.collection)
        return value

    def start(self, *args, **kwargs):
        self.collection = {}

    def value(self, *args, **kwargs):
        return self.collection


class Value(object):
    """
    Returns the value provided for an element
    """
    def value(self, value, *args, **kwargs):
        return value


class DateValue(BaseDecorator):

    def __init__(self, format, obj=None, *args, **kwargs):
        self.obj = obj if obj is not None else Value()
        super(DateValue, self).__init__(self.obj, *args, **kwargs)
        self.format = format

    def value(self, value, *args, **kwargs):
        """
        Takes a string value and returns the Date based on the format
        """
        from datetime import datetime
        value = self.obj.value(value, *args, **kwargs)
        try:
            rv = datetime.strptime(value, self.format)
        except ValueError as _:  # noqa
            rv = None
        return rv


class KeyValue(BaseDecorator):
    """
    Returns a key-value pair for an elements value, where the key is set during initialization
    """
    def __init__(self, key=None, obj=None, *args, **kwargs):
        obj = obj if obj is not None else Value()
        super(KeyValue, self).__init__(obj, *args, **kwargs)
        self.key = key

    def start(self, name, *args, **kwargs):
        if self.key is None:
            self.key = name
        return self.obj.start(*args, **kwargs) if hasattr(self.obj, 'start') else None

    def value(self, value, *args, **kwargs):
        value = self.obj.value(value, *args, **kwargs)
        return {self.key: value}


class RecursiveKeyValueCollector(KeyValueCollector, SingletonCollectorMixIn):
    def __init__(self, *args, **kwargs):
        super(RecursiveKeyValueCollector, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        try:
            v = super(RecursiveKeyValueCollector, self).__getitem__(item)
        except KeyError as _:  # noqa
            v = RecursiveKeyValueCollector(*self.args, **self.kwargs)
            self[item] = v
        return v

