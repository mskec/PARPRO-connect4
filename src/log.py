

class Log:

    DEBUG = False

    def __init__(self, owner_name):
        self._owner_name = owner_name

    @staticmethod
    def info(message):
        print message

    def debug(self, message):
        if Log.DEBUG:
            print '%s: %s' % (self._owner_name, message)
