#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests the worker by sending it information to process and seeing
the response from a worker
"""

from multiprocessing import Process
import pytest
import sys
import time
import zmq

from text_transformation.worker import Worker

def test_start_up():
    w = Worker("worker", {})
    w.start()
    w.stop()

def test_no_transformations():
    w = Worker("worker", {})
    # create sender
    sender = w.context.socket(zmq.PUSH)
    sender.bind("ipc://./.workerpush.ipc")
    # create receiver
    receiver = w.context.socket(zmq.PULL)
    receiver.bind("ipc://./.workerpull.ipc")
    # send json data
    w.start()
    for i in range(20):
        sender.send_pyobj(
            (i, {"type": "text", "data": "", "transformations":{}})
        )
        assert receiver.recv_pyobj() == (i, {})
    w.stop()

def test_with_transformations():
    def t1(*args, **kwargs):
        return "cat"
    def t2(*args, **kwargs):
        return [1, 2, 3]
    def t3(arg1, *args, **kwargs):
        return arg1
    tfs = {"t1": t1, "t2": t2, "t3": t3}
    w = Worker("worker", tfs)
    # create sender
    sender = w.context.socket(zmq.PUSH)
    sender.bind("ipc://./.workerpush.ipc")
    # create receiver
    receiver = w.context.socket(zmq.PULL)
    receiver.bind("ipc://./.workerpull.ipc")
    # send json data
    w.start()
    d = {"type": "text", "data": "", "transformations":{}}

    d["transformations"] = {"t1": 1, "t3": "gerg"} 
    sender.send_pyobj((1, d))
    assert receiver.recv_pyobj() == (1, {"t1": "cat", "t3": "gerg"})

    d["transformations"] = {"t2": True}
    sender.send_pyobj((5, d))
    assert receiver.recv_pyobj() == (5, {"t2": [1, 2, 3]})
    w.stop()
"""
def _test_start_up_multiple_workers():
    workers = [Process(target=run_worker, args=("W")) for i in range(10)]
    time.sleep(1)
    # end processes
    for w in workers:
        w.terminate()
        w.join()


def _test_one_worker_transform_no_transformations():
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


def _test_multiple_workers_transform_no_transformations():
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
"""
