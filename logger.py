from constants.debugging_flags import *


class Logger(object):

    def __init__(self, origin, origin_flag):
        self.origin = origin
        self.origin_flag = origin_flag

    def debug(self, method, msg):
        if DEBUG and self.origin_flag:
            print "[Origin: %s, method: %s] %s" % (self.origin, method, str(msg))
