from UserDict import IterableUserDict

__author__ = 'brent'

class BaseDecorator(object):
    def __init__(self, obj):
        self.obj = obj

        def start(*args, **kwargs):
            return self.obj.start(*args, **kwargs)
        if hasattr(obj, 'start') and not hasattr(self, 'start'):
            setattr(self, 'start', start)

        def value(*args, **kwargs):
            return self.obj.value(*args, **kwargs)
        if hasattr(obj, 'value') and not hasattr(self, 'value'):
            setattr(self, 'value', value)

        def end(*args, **kwargs):
            return self.obj.end(*args, **kwargs)
        if hasattr(obj, 'end') and not hasattr(self, 'end'):
            setattr(self, 'end', end)

class CaptureKeyValue(BaseDecorator, IterableUserDict):
    def __init__(self, obj, dictionary_callback=None):
        super(CaptureKeyValue, self).__init__(obj)
        self.data = obj
        # the callback allows the owner to swap out dictionaries
        if dictionary_callback is not None:
            self.dictionary_callback = dictionary_callback
        else:
            dd = {} # return a the same dictionary for every elements
            self.dictionary_callback = lambda: dd

    def value(self, value, *args, **kwargs):
        print value
        dict_value = self.data.value(value)
        self.dictionary_callback().update(dict_value)
        return self.dictionary_callback()


class CaptureListItem(BaseDecorator, IterableUserDict):
    def __init__(self, obj, list_callback=None):
        super(CaptureListItem, self).__init__(obj)
        self.data = obj
        # the callback allows the owner to swap out lists
        if list_callback is not None:
            self.list_callback = list_callback
        else:
            ll = []
            self.list_callback = lambda: ll  # Return the same list for every elements

    def value(self, value, *args, **kwargs):
        value = self.data.value(value)
        self.list_callback().append(value)
        return self.list_callback()

