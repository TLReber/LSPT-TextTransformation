#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests the worker by sending it information to process and seeing
the response from a worker
"""

from multiprocessing import Process
import pytest
import time
import zmq

from text_transformation.worker import Worker

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


def run_worker(name):
    # run as separate process
    w = Worker(name)
    w.start()


def test_start_up_worker():
    # run worker as separate process, wait then end it
    worker_p = Process(target=run_worker, args=("W"))
    time.sleep(1)
    # end processes
    worker_p.terminate()
    worker_p.join()


def test_start_up_multiple_workers():
    workers = [Process(target=run_worker, args=("W")) for i in range(10)]
    time.sleep(1)
    # end processes
    for w in workers:
        w.terminate()
        w.join()


def test_one_worker_transform_no_transformations():
    context = zmq.Context()
    # create sender
    sender = context.socket(zmq.PUSH)
    sender.bind("ipc:///W-push")
    # create receiver
    receiver = context.socket(zmq.PULL)
    receiver.bind("ipc:///W-pull")
    receiver.RCVTIMEO = 1000
    worker_p = Process(target=run_worker, args=("W"))

    # send json data
    for i in range(20):
        sender.send_json(
            {"id": i, "type": "text", "data": "", "transformations": []}
        )
        assert receiver.recv_json() == {"id": i, "transformations": []}
    # end processes
    worker_p.terminate()
    worker_p.join()


def test_multiple_workers_transform_no_transformations():
    # makes a blocking call, don't test until ready
    context = zmq.Context()
    # create sender
    sender = context.socket(zmq.PUSH)
    sender.bind("ipc:///W-push")
    # create receiver
    receiver = context.socket(zmq.PULL)
    receiver.bind("ipc:///W-pull")
    receiver.RCVTIMEO = 1000
    workers = [Process(target=run_worker, args=("W")) for i in range(10)]

    # send json data
    for i in range(200):
        sender.send_json(
            {"id": i, "type": "text", "data": "", "transformations": []}
        )
        assert receiver.recv_json() == {"id": i, "transformations": []}
    # end processes
    for w in workers:
        w.terminate()
        w.join()
