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
            (i, {"type": "text", "data": "", "transformations": {}})
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
    d = {"type": "text", "data": "", "transformations": {}}

    d["transformations"] = {"t1": 1, "t3": "gerg"}
    sender.send_pyobj((1, d))
    assert receiver.recv_pyobj() == (1, {"t1": "cat", "t3": "gerg"})

    d["transformations"] = {"t2": True}
    sender.send_pyobj((5, d))
    assert receiver.recv_pyobj() == (5, {"t2": [1, 2, 3]})
    w.stop()
