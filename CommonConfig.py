import sys
import os
import ConfigParser

class CommonConfig:

    VERSION = "0.1"
    cfg = None

    def __init__(self,filename=None):
        if filename is None:
            # load it from the current directory
             filename = os.path.join(os.path.dirname(__file__), "esgob.ini")
        if os.path.exists(filename) is False:
            raise Exception("Config not found at: %s" % (filename))
        self.cfg = ConfigParser.RawConfigParser()
        self.cfgname = filename
        self.cfg.read(self.cfgname)
        return

    def getstr(self,section,key):
        val = self.cfg.get(section,key)
        if len(val) == 0:
            raise Exception("Config value for %s/%s missing" % (section,key))
        return val

    def getint(self,section,key):
        return int(self.getstr(section,key))

    def getbool(self,section,key):
        return self.cfg.getboolean(section,key)