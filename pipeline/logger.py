import time

class logging(object):
    def __init__(self, path):
        self.path = path
        self.logger = open(path, "a")

    def info(self, message):
        self.logger.write("Info  [%s]: %s\n"  % (self.prefix, message))
        self.logger.flush()

    def warn(self, message):
        self.logger.write("Warn  [%s]: %s\n"  % (self.prefix, message))
        self.logger.flush()

    def error(self, message):
        self.logger.write("Error [%s]: %s\n" % (self.prefix, message))
        self.logger.flush()

    @property
    def prefix(self): 
        return "%s %s" % ((time.strftime("%Y-%m-%d", time.localtime()), time.strftime("%H:%M:%S", time.localtime())))
