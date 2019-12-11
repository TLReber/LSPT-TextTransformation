#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File that houses all the entry points.There is currently only one entry point.
That entry point is run_server which starts up a scheduler and a variable
number of workers
"""
from multiprocessing import Process
import sys

from text_transformation.scheduler import Scheduler
from text_transformation.worker import Worker
from text_transformation.transformations import title, stripped, ngrams


def run_server():
    """
    Entry point that starts up several workers and a scheduler. The Scheduler
    listends for http requests and delegates the requests off to workers
    """
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
        Process(target=run_worker, args=((s.name,))) for _ in range(w_count)
    ]
    print(f"======== Running {w_count} Worker(s) =========")
    for wp in worker_processes:
        wp.start()
    # listen for incomming messages
    s.host("0.0.0.0", port)
    s.stop()
    for wp in worker_processes:
        wp.terminate()


def run_worker(scheduler_name: str):
    """
    This is a helper function that runs on a separate process. It spins up a
    worker that communicates with a scheduler specified scheduler name 

    Args: 
        scheduler_name: name of scheduler the worker is communicating with
    """
    tf = {"title": title, "stripped": stripped, "grams": ngrams}
    try:
        w = Worker(scheduler_name, tf)
        w.listen()
    except KeyboardInterrupt:
        pass
