"""
pipeline

This package contains pipelines (transcriptome, exome, genome etc.) for bioinformation analysis.

author: liuwei
e-mail: liuweiathust@foxmail.com
create-date: 2012-11-02
"""

__title__   = "pipeline"
__author__  = "liuwei"
__email__   = "liuweiathust@foxmail.com"

from .application import Application
from .project import Project
from .logger import logging
from .environment import Environment,Configure,JSONParser,get_environment

__all__ = ["Application", "running_mode", "Project", "logging", "Environment", "Configure", "JSONParser", "get_environment"]
