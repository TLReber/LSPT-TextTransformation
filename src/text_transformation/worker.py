#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module houses the Worker component which is used by the scheduler to
increase throughput by running tasks in parallel
"""

from threading import Thread
from bs4 import BeautifulSoup
import zmq


class Worker:
    """
    Takes in requests from the scheduler and performs them and funnels the
    results back to the scheduler.

    Attributes:
        context(zmq.Context): context used by zmq to create the sockets that
            push/pull information to/from a scheduler
        listen_thread(Thread): runs self.listen in background to test worker
            threads without too much hassle
        scheduler_name(str): name of scheduler receives requests from and
            pushes results to
        transformations(dict): string of transformation names
    """

    def __init__(self, scheduler_name: str, transformations: dict):
        self.scheduler_name = scheduler_name
        self.transformations = transformations
        # create zmq requester object
        self.context = zmq.Context()
        # listening thread set-up
        self.listen_thread = Thread(target=self.listen)

    def start(self):
        """
        Non-blocking call that starts a thread which listens for requests from 
        the scheduler and pushes results back to the scheduler
        """
        self.listen_thread.start()

    def stop(self):
        """
        The listen call blocks indefinitly, stop can be invoked (from another
        thread) to end the self.listen call
        """
        ender = self.context.socket(zmq.REQ)
        ender.connect(f"inproc://{self.scheduler_name}")
        ender.send_pyobj((None, None))
        self.listen_thread.join()
        self.context.destroy()

    def listen(self):
        """
        Listens for incoming requests by a scheduler. This call blocks
        indefinitely (or until self.stop is invoked)
        """
        receiver = self.context.socket(zmq.PULL)
        sender = self.context.socket(zmq.PUSH)
        ender = self.context.socket(zmq.REP)

        receiver.connect(f"ipc://./.{self.scheduler_name}push.ipc")
        sender.connect(f"ipc://./.{self.scheduler_name}pull.ipc")
        ender.bind(f"inproc://{self.scheduler_name}")

        # makes a poller
        poller = zmq.Poller()
        poller.register(ender, zmq.POLLIN)
        poller.register(receiver, zmq.POLLIN)
        while True:
            socks = dict(poller.poll())
            if ender in socks and socks[ender] == zmq.POLLIN:
                msg = ender.recv_pyobj()
                return
            elif receiver in socks and socks[receiver] == zmq.POLLIN:
                r_id, data = receiver.recv_pyobj()
                data = self.on_recv(data)
                sender.send_pyobj((r_id, data))

    def on_recv(self, data):
        """
        Handler of json data it receives from listen

        Args:
            data(dict): dictionary representation of the json required to be
                transformed

        Returns:
            (dict): response to the transformation
        """
        stop_words = [
            "the",
            "of",
            "to",
            "a",
            "and",
            "in",
            "said",
            "for",
            "that",
            "was",
            "on",
            "he",
            "is",
            "with",
            "at",
            "by",
            "it",
            "from",
            "as",
            "be",
            "were",
            "an",
            "have",
            "his",
            "but",
            "has",
            "are",
            "not",
            "who",
            "they",
            "its",
            "had",
            "will",
            "would",
            "about",
            "i",
            "been",
            "this",
            "their",
            "new",
            "or",
            "which",
            "we",
            "more",
            "after",
            "us",
            "percent",
            "up",
            "one",
            "people",
        ]
        soup = BeautifulSoup(data["data"], "html.parser")
        tfs = {}
        for name, arg in data["transformations"].items():
            if name not in self.transformations:
                continue
            else:
                tf = self.transformations[name]
                tfs[name] = tf(
                    arg, soup_instance=soup, stop_word_list=stop_words
                )
        return tfs
