import sys
import os.path
import logging
import running_mode

class Application(object):
    """
    pipeline.application.Application is a framework for running (transcriptome|exome|genome) analysis pipeline
    """
    def __init__(self):
        self.errors = []
        self.infos = []
        self.warns = []
        self._running_mode = None

    @property
    def logger(self):
        """the logger property."""
        return self.environment["logger"]

    def log_information(self):
        self.log_warnings()
        self.running_mode.log_information()
        self.exit_when_error()

    @property
    def running_mode(self):
        return self._running_mode

    @running_mode.setter
    def running_mode(self, _running_mode):
        self._running_mode = _running_mode(self)

    def log_warnings(self):
        self.running_mode.log_warnings()

    def exit_when_error(self):
        self.running_mode.exit_when_error()

    def run(self, script, on_finish, on_error):
        self.running_mode.process_command(command, on_finish, on_error)

    def finish(self):
        self.infos.append("Application finished.")
        self.log_information()

    def __str__(self):
        return "Application"
