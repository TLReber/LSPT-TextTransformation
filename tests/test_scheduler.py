#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests the scheduler by stubbing the worker an echo server and
verifying that the json request coming in the same json request coming out
"""

import asyncio
from multiprocessing import Process, Queue
import pytest
import requests
import sys
import time
import zmq

from text_transformation.scheduler import Scheduler


def run_echo_worker(name, error_q):
    context = zmq.Context()
    try:
        # receive messages from
        receiver = context.socket(zmq.PULL)
        receiver.connect(f"ipc://./.{name}push.ipc")
        # send messages to
        sender = context.socket(zmq.PUSH)
        sender.connect(f"ipc://./.{name}pull.ipc")
        while True:
            reply = receiver.recv_pyobj()
            sender.send_pyobj(reply)
    except Exception:
        context.destroy()
        error_q.put("ERROR")
        raise Exception


async def run_requester(scheduler, num_requests):
    replies, _ = await asyncio.wait(
        [
            scheduler.transform({"echo": [1, 2, 3], "index": i})
            for i in range(num_requests)
        ]
    )
    assert len(replies) == num_requests
    for r in replies:
        assert r.result()["echo"] == [1, 2, 3]


def test_start_up():
    s = Scheduler("scheduler")
    s.start()
    s.stop()


def test_echo_one_worker():
    error_q = Queue()
    s = Scheduler("scheduler")
    s.start()
    worker_p = Process(target=run_echo_worker, args=("scheduler", error_q))
    worker_p.start()

    # make requests
    asyncio.run(run_requester(s, 100))
    assert error_q.empty()
    # end processes
    worker_p.terminate()
    s.stop()


def test_multiple_workers():
    error_q = Queue()
    s = Scheduler("scheduler")
    s.start()
    workers = [
        Process(target=run_echo_worker, args=("scheduler", error_q))
        for i in range(10)
    ]
    for w in workers:
        w.start()
    time.sleep(0.5)  # make sure that all sockets connected first

    asyncio.run(run_requester(s, 100))

    assert error_q.empty()
    # end processes
    for w in workers:
        w.terminate()
    s.stop()
