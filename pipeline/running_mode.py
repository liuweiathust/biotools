import os
import sys
import time
from subprocess import Popen

class running_mode(object):
    def __init__(self, application):
        self.application = application

    def run_command(self, command):
        """
        Script runner for running command line.
        Argument 'command' must be real executable command line
        This function will run command using subprocess.Popen wrapper
        """
        env = self.application.environment["environments"]
        return Popen(command, shell=True, env=env).wait()

class run(running_mode):
    def process_command(self, command, on_finish="finished", on_error="failed"):
        """
        
        """
        try:
            start = time.time()
            self.application.infos.append("[%s] start running command:    %s" % (time.strftime("%H:%M:%S", time.localtime()), command))

            self.application.log_information()
            
            retcode = self.run_command(command)
            if retcode != 0:
                raise Exception("exitcode is not zero!")
            
            end = time.time()
            self.application.infos.append("[%s] finished running command: %s" % (time.strftime("%H:%M:%S", time.localtime()), raw_script))
            span = end - start
            self.application.infos.append("(finish %s in %d seconds)" % (raw_script, span))
            self.application.infos.append(self.on_finish)
            
        except Exception as e:
            self.application.errors.append(self.on_error)
            if locals().has_key("retcode"):
                self.application.errors.append("Error happends when running: %s (retcode: %d)\n%s" % (command, retcode, e))
            else:
                self.application.errors.append("Error happends when running: %s\n%s" % (command, e))
        self.application.log_information()

    def log_information(self):
        if self.application.infos:
            for info in self.application.infos:
                self.application.logger.info(info)
        self.application.infos = []

    def log_warnings(self):
        if self.application.warns:
            for warn in self.application.warns:
                self.application.logger.warn(warn)
        self.application.warns = []

    def exit_when_error(self):
        if self.application.errors:
            self.application.logger.error("Error (%d errors):" % len(self.application.errors) - 1)
            for i, error in enumerate(self.application.errors):
                self.application.logger.error("  %2d. %s" % (i+1, error))
            self.application.errors = []
            sys.exit(1)

class debug(running_mode):
    def process_command(self, command, on_finish="finish", on_error="error"):
        self.application.infos.append(command)
        self.application.log_information()

    def log_information(self):
        if self.application.infos:
            for info in self.application.infos:
                print(info)
            sys.stdout.flush()
            self.application.infos = []

    def log_warnings(self):
        if self.application.warns:
            for info in self.application.infos:
                self.application.logger.info(info)
            self.application.warns = []

    def exit_when_error(self):
        if self.application.errors:
            print("Errors:")
            for i, error in enumerate(self.application.errors):
                print("    %2d. %s" % (i+1, error))
            sys.stdout.flush()
            self.application.errors = []
            sys.exit(1)    
