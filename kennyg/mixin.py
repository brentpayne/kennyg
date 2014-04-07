__author__ = 'brent'



class SingletonCollectorMixIn(object):
    def __init__(self, *args, **kwargs):
        super(SingletonCollectorMixIn, self).__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        pass # do not reset the value on start

