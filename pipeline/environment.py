"""
environments

Defined some environment variables for running pipeline.
These environment variables will be loaded when analysis started.

author: liuwei
email: liuweiathust@foxmail.com
createDate: 2012-11-06
"""
import json
import re
import time
import os
import os.path
import logger
import argparse

class Environment(object):
    """
    Build pipeline environments
    Using singleton patterns to ensure only one Environment object in life-circle
    You can get instance of Environment using Environment.getInstance()
    """
    def __init__(self):
        raise "You can get instance of Environment using Environment.getInstance()"

    __instance = None

    @staticmethod
    def get_instance():
        if not Environment.__instance:
            Environment.__instance = object.__new__(Environment)
        return Environment.__instance

    @property
    def configure(self):
        """the configure property."""
        return self._configure
    
    @configure.setter
    def configure(self, value):
        self._configure = value

    @property
    def project_dir(self):
        """the project_dir property."""
        return self.configure["paths"]["project_dir"]

    def __getattr__(self, name):
        """
        Using proxy pattern for fetch environments from configure
        """
        if name in self.configure:
            return self.configure[name]
        else:
            raise AttributeError, name

    def __getitem__(self, name):
        """
        Using proxy pattern for fetch environments from configure
        """
        if name in self.configure:
            return self.configure[name]
        elif name == "project_dir":
            return self.project_dir
        else:
            raise KeyError, name

class JSONParser(object):
    """
    JSONParser for parsing pipeline configure file
    """
    comment_re = re.compile('(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?', re.DOTALL | re.MULTILINE)

    def __init__(self, json_string):
        self.raw_content = json_string
        self.content = json_string
        self.remove_comments()    

    def remove_comments(self):
        """
        Considering configure file is a JSON file, comments must be removed before parse 
        """
        match = JSONParser.comment_re.search(self.content)
        while match:
            self.content = self.content[:match.start()] + self.content[match.end():]
            match = JSONParser.comment_re.search(self.content)

    @property
    def result(self):
        """
        Return parsed content with pythonic data structures
        """
        return json.loads(self.content)

class Configure(object):
    """
    Pipeline configure file parser
    """
    def __init__(self, configure_file):
        self.configure_file = configure_file
        self.configure = self.parse_configure_file()
        self.expand_paths()
        self.update_analysis()
        self.update_environments()
        self.add_logger()

    def parse_configure_file(self):
        content = open(self.configure_file).read()
        return JSONParser(content).result

    def expand_paths(self):
        """
        Configure file's paths are relative paths, these must be converted to absolute paths
        """
        paths = self.configure["paths"]
        if not os.path.isdir(paths["project_dir"]):
            raise """{"paths": {"project_dir": abs-path-to-project-dir}} must be set"""
        for name, path in paths.iteritems():
            if name != "project_dir":
                paths[name] = os.path.join(paths["project_dir"], path)
        self.configure["paths"] = paths

    def update_analysis(self):
        """
        Update analysis information
        Includes project created date, time, etc.
        """
        self.configure["analysis"].update({ "date": self.date, "time": self.time })

    def add_logger(self):
        if not os.path.isdir(self.configure["paths"]["log_dir"]):
            os.mkdir(self.configure["paths"]["log_dir"])
        log_file = os.path.join(self.configure["paths"]["log_dir"], "pipeline.log")
        self.configure["logger"] = logger.logging(log_file)

    def update_environments(self):
        """
        Merge user defined environment variables and system default environment variables
        """
        temp = self.configure["environments"]
        self.configure["environments"] = os.environ
        for env, value in temp.iteritems():
            if os.environ.has_key(env):
                self.configure["environments"][env] = ":".join(value) + ":" + self.configure["environments"][env]
            else:
                self.configure["environments"][env] = ":".join(value)

        for soft, path in self.configure["softwares"].iteritems():
            if not os.path.dirname(path) in self.configure["environments"]["PATH"].split(":"):
                self.configure["environments"]["PATH"] = os.path.dirname(path) + ":" + self.configure["environments"]["PATH"] 

    @property
    def date(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    @property
    def time(self):
        return time.strftime("%H:%M:%S", time.localtime())
      

def get_environment(configure_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.json")):
    environment = Environment.get_instance()
    configure = Configure(configure_file)
    environment.configure = configure.configure
    return environment

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="environments and configure file parser for pipeline")
    parser.add_argument(
        "-c", "--configure", 
        dest="configure", 
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.json"),
        help="the path to configure file.")
    args = parser.parse_args()

    environment = get_environment(args.configure)
    print (environment.configure)
