#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module houses the Scheduler component which is the front facing api server
"""

from aiohttp import web
import asyncio
import sys
from threading import Thread
import zmq


class Scheduler:
    """
    Front-facing server that handles api requests and delegates work to workers.
    Uses asyncio to handle post requests. The api is /transform(POST). This
    is the only post request; it takes in a description of the data, the applied 
    transformations to apply and targets to post the transformations to. If 
    there are no targets, then the transformation is returned back to "POSTER" 
    of input

    Attributes:
        address(tuple):(str, int), (ip, port)
        app(web.Application): helper tool to setup http request system
        name(str): string identifier unique across processes
        results(dict): key of unique work request id, value of future
        request_id(int): used to assign unique ids for results
        listen_thread(Thread): runs self.listen in background to make 
            self.results awaitable
        
    """

    def __init__(self, name: str):
        self.name = name
        # create zmq requester object
        self.context = zmq.Context()
        self.requester = self.context.socket(zmq.PUSH) 
        # listening thread set-up
        self.request_id = 0
        self.results = {}
        self.listen_thread = Thread(target=self.listen)

        self.app = web.Application()
        # adding current routes
        routes = [
            web.post(f"/transform", self.transform_route)
        ]
        self.app.add_routes(routes)

    def host(self, ip, port):
        """
        Starts web app
        """
        web.run_app(self.app, host=ip, port=port)

    def start(self):
        """
        Starts self.listen_thread and app
        """
        self.requester.bind(f"ipc://./.{self.name}push.ipc")
        self.listen_thread.start()

    def stop(self):
        """
        Ends self.listen_thread
        """
        ender = self.context.socket(zmq.PUSH)
        ender.connect(f"ipc://./.{self.name}pull.ipc")
        ender.send_pyobj((None, None))
        self.listen_thread.join()
        self.context.destroy()
    
    def listen(self):
        receiver = self.context.socket(zmq.PULL)
        receiver.bind(f"ipc://./.{self.name}pull.ipc")
        while True:
            result_id, data = receiver.recv_pyobj()
            if result_id is None:
                # signal that its time to stop
                break
            # recover future id
            # need to lock?
            loop = self.results[result_id].get_loop()
            loop.call_soon_threadsafe(
                self.results[result_id].set_result(data))
            

    async def transform_route(self, request):
        json = await self.transform(await request.json())
        return web.json_response(json)

    async def transform(self, json):
        """
        HTTP request is routed here, what is expected of request is are these 
        attributes. type: describes the type of data to be parsed (currently
        only text and html. data: the raw data passed in (must match type).
        transformed: list of transformations to alter the data

        Args:
            request(HTTPRequest): request of invoker of http-request

        """
        # send to work
        r_id = self.request_id
        self.results[r_id] = asyncio.Future()
        self.request_id += 1
        self.requester.send_pyobj((r_id, json))
        result = await self.results[r_id]
        del self.results[r_id]
        return result

