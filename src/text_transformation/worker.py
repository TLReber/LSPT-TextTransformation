#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from bs4 import BeautifulSoup
import zmq

class Worker:
    """
    Takes in requests from the scheduler and performs them and funnels the
    results back to the scheduler.

    Attributes:
        scheduler_name(str): name of scheduler receives requests from and
            pushes results to
        transformations(dict): string of transformation names
    """

    def __init__(
        self, scheduler_name: str, transformations: dict
    ):
        self.scheduler_name = scheduler_name
        self.transformations = transformations
        # create zmq requester object
        self.context = zmq.Context()
        # listening thread set-up
        self.listen_thread = Thread(target=self.listen)

    def start(self):
        """
        Blocking call that listens for requests from the scheduler and pushes
        results back to the scheduler
        """
        self.listen_thread.start()

    def stop(self):
        ender = self.context.socket(zmq.REQ)
        ender.connect(f"inproc://{self.scheduler_name}")
        ender.send_pyobj((None, None))
        self.listen_thread.join()
        self.context.destroy()


    def listen(self):
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
        stop_words = [] 
        soup = BeautifulSoup(data["data"], "html.parser") 
        tfs = {}
        for name, arg in data["transformations"].items():
            if name not in self.transformations:
                continue
            else:
                tf = self.transformations[name]
                tfs[name] = tf(
                        arg, 
                        soup_instance=soup, 
                        stop_word_list=stop_words)
        return tfs
