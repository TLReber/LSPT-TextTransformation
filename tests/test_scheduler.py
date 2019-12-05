#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests the scheduler by stubbing the worker an echo server and
verifying that the json request coming in the same json request coming out
"""

from multiprocessing import Process, Queue
import pytest
import requests
import time
import zmq

from text_transformation.scheduler import Scheduler

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"


def run_scheduler(name, address, duration, q):
    # run a scheduler for specified duration separate process
    try:
        s = Scheduler(name, address)
        s.start()
        time.sleep(duration)
        s.stop()
    except Exception:
        q.put("ERROR")
        raise Exception


def run_echo_worker(name):
    context = zmq.Context()
    # receive messages from
    receiver = context.socket(zmq.PULL)
    receiver.connect(f"ipc:///{name}-push")
    # send messages to
    sender = context.socket(zmq.PUSH)
    sender.connect(f"ipc:///{name}-pull")
    while True:
        msg = receiver.recv_json()
        sender.send_json(msg)


def run_requester(address, num_requests):
    ip, port = address
    address = f"http://{ip}:{port}/transform"
    for i in range(num_requests):
        r = requests.post(address, json={"echo": [1, 2, 3], "index": i})
        assert r.status_code == 200
        assert r.json == {"echo": [1, 2, 3], "index": i}

def test_scheduler_start_up():
    s = Scheduler("scheduler")
    s.start()
    s.stop()

def _test_scheduler_echo_one_worker():
    # run_scheduler as separate process
    scheduler_p = Process(
        target=run_scheduler, args=("scheduler", ("127.0.0.1", 8080))
    )
    worker_p = Process(target=run_echo_worker, args=("scheduler"))
    time.sleep(1)  # takes time to spin up server
    # make requests
    run_requester(("127.0.0.1", 8080), 10)
    # end processes
    scheduler_p.terminate()
    worker_p.terminate()
    scheduler_p.join()
    worker_p.join()


def _test_scheduler_multiple_workers():
    scheduler_p = Process(
        target=run_scheduler, args=("scheduler", ("127.0.0.1", 8080))
    )
    workers = [
        Process(target=run_echo_worker, args=("scheduler")) for i in range(10)
    ]
    time.sleep(1)  # takes time to spin up server
    # make requests
    run_requester(("127.0.0.1", 8080), 20)
    # end processes
    scheduler_p.terminate()
    scheduler_p.join()
    for w in workers:
        w.terminate()
        w.join()


def _test_scheduler_multiple_workers_multiple_requests():
    scheduler_p = Process(
        target=run_scheduler, args=("scheduler", ("127.0.0.1", 8080))
    )
    workers = [
        Process(target=run_echo_worker, args=("scheduler")) for i in range(10)
    ]
    time.sleep(1)  # takes time to spin up server
    # makes a bunch of requests in parallel (20 clients at once)
    requesters = [
        Process(target=run_requester, args=(("127.0.0.1", 8080), 15))
        for i in range(20)
    ]
    for r in requesters:
        r.join()
    scheduler_p.terminate()
    scheduler_p.join()
    for w in workers:
        w.terminate()
        w.join()
