#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
file that houses all the entry points. The default scheduler script is 
run_scheduler which spins up a scheduler to take in api requests. The default
worker script is run_worker which spins up a worker to help the scheduler
processes incoming requests
"""
from multiprocessing import Process
import sys

from text_transformation.scheduler import Scheduler
from text_transformation.worker import Worker
from text_transformation.transformations import title, stripped, ngrams


def run_server():
    name = None
    port = None
    w_count = None
    if len(sys.argv) == 4:
        name, port, w_count = tuple(sys.argv[1:])
        port = int(port)
        w_count = int(w_count)
    else:
        print("Invalid Arguments:")
        print("text-trans-server <name> <port> <num_workers>")
        return
    # start scheduler
    s = Scheduler(name)
    s.start()
    # start workers
    worker_processes = [
        Process(target=run_worker, args=((s.name,)))
        for _ in range(w_count)
    ]
    print(f"======== Running {w_count} Worker(s) =========")
    for wp in worker_processes:
        wp.start()
    # listen for incomming messages
    s.host("0.0.0.0", 8080)
    s.stop()
    for wp in worker_processes:
        wp.terminate()

def run_worker(process_name):
    """
    The entry point to start the worker from the terminal. Command line
    arguments are expected for run_worker to work. The only argument is the name
    of the scheduler. The name of the scheduler facilitates communication
    between the scheduler and the worker
    """
    tf = {
        "title": title,
        "stripped": stripped,
        "grams": ngrams
    }
    try:
        w = Worker(process_name, tf)
        w.listen()
    except KeyboardInterrupt:
        pass
