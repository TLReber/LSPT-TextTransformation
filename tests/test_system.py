#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests the full system without api calls
"""

import asyncio
from multiprocessing import Process
import pytest

from text_transformation.scheduler import Scheduler
from text_transformation.entry_points import run_worker


def start_system(num_workers: int):
    s = Scheduler("system")
    s.start()
    workers = [
        Process(target=run_worker, args=((s.name,))) for _ in range(num_workers)
    ]
    for wp in workers:
        wp.start()
    return (s, workers)


def stop_system(s, workers):
    s.stop()
    for wp in workers:
        wp.terminate()


async def check_request(s, request, exp_reply):
    reply = await s.transform(request)
    assert reply == exp_reply


async def check_requests(s, requests, exp_replys):
    await asyncio.gather(
        *tuple(
            [
                check_request(s, req, rep)
                for req, rep in zip(requests, exp_replys)
            ]
        )
    )


def test_start_up():
    for num_workers in range(5):
        s, workers = start_system(1)
        stop_system(s, workers)


def test_empty_json():
    num_workers = 3
    s, workers = start_system(num_workers)
    request = {"type": "html", "data": "", "transformations": {}}
    exp_reply = {}
    asyncio.run(check_request(s, request, exp_reply))
    stop_system(s, workers)


def test_empty_json_simultaneous_requests():
    num_workers = 3
    s, workers = start_system(num_workers)
    num_requests = 2000
    request = {"type": "html", "data": "", "transformations": {}}
    exp_reply = {}

    requests = [request for _ in range(num_requests)]
    replies = [exp_reply for _ in range(num_requests)]
    asyncio.run(check_requests(s, requests, replies))
    stop_system(s, workers)


def test_simple_json():
    num_workers = 3
    s, workers = start_system(num_workers)
    request = {
        "type": "html",
        "data": """<html>
                <head> <title>TITLE</title> </head>
                <p>
                    hello hello world this is some test, go parse this 
                </p>
            </hmtl>""",
        "transformations": {"stripped": True, "grams": [1, 3], "title": True},
    }
    exp_reply = {
        "grams": {
            1: {
                "title": [0],
                "go": [8],
                "hello": [1, 2],
                "parse": [9],
                "some": [6],
                "test": [7],
                "world": [3],
            },
            3: {
                "title hello hello": [0],
                "hello hello world": [1],
                "some test go": [6],
                "test go parse": [7],
            },
        },
        "stripped": "title hello hello world some test go parse",
        "title": "TITLE",
    }
    asyncio.run(check_request(s, request, exp_reply))
    stop_system(s, workers)


def test_simple_json_simultaneous_requests():
    num_workers = 3
    num_requests = 2000
    s, workers = start_system(num_workers)
    request = {
        "type": "html",
        "data": """<html>
                <p>
                    hello hello world this is some test, go parse this 
                </p>
            </hmtl>""",
        "transformations": {"stripped": True, "grams": [1, 3], "title": True},
    }
    exp_reply = {
        "grams": {
            1: {
                "go": [7],
                "hello": [0, 1],
                "parse": [8],
                "some": [5],
                "test": [6],
                "world": [2],
            },
            3: {
                "hello hello world": [0],
                "some test go": [5],
                "test go parse": [6],
            },
        },
        "stripped": "hello hello world some test go parse",
        "title": "",
    }
    requests = [request for _ in range(num_requests)]
    replies = [exp_reply for _ in range(num_requests)]
    asyncio.run(check_requests(s, requests, replies))
    stop_system(s, workers)
