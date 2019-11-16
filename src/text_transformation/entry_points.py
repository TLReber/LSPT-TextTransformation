#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
file that houses all the entry points. The default scheduler script is 
run_scheduler which spins up a scheduler to take in api requests. The default
worker script is run_worker which spins up a worker to help the scheduler
processes incoming requests
"""
import sys
from text_transformation.server import Server


def run_scheduler():
    """
    The entry point to start the scheduler from the terminal. Command line 
    arguments are expected for run_scheduler to work. The first argument is
    the ip address and port number (ex: 127.0.0.1:8080). The second argument
    is the name of the scheduler which is used to workers can communicate with
    the scheduler
    """
    pass


def run_worker():
    """
    The entry point to start the worker from the terminal. Command line
    arguments are expected for run_worker to work. The only argument is the name
    of the scheduler. The name of the scheduler facilitates communication
    between the scheduler and the worker
    """
    pass
