#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module houses the Scheduler component which is the front facing api server

"""


class Scheduler:
    """
    Front-facing server that handles api requests and delegates work to workers.
    Uses asyncio to handle post requests. The api is /transform(POST). This
    is the only post request; it takes in a description of the data, the applied 
    transformations to apply and targets to post the transformations to. If 
    there are no targets, then the transformation is returned back to "POSTER" 
    of input

    Attributes:
        app(web.Application): helper tool to setup http request system
        name(str): string identifier unique across processes
        results(dict): key of unique work request id, value of future
        request_id(int): used to assign unique ids for results
        listen_thread(Thread): runs self.listen in background to make 
            self.results awaitable
        
    """

    def __init__(self, name: str, address: tuple):
        pass

    def start(self):
        """
        Starts self.listen_thread and app
        """
        pass

    def stop(self):
        """
        Ends self.listen_thread
        """
        pass

    async def transform(self, request):
        """
        HTTP request is routed here, what is expected of request is are these 
        attributes. type: describes the type of data to be parsed (currently
        only text and html. data: the raw data passed in (must match type).
        transformed: list of transformations to alter the data

        Args:
            request(HTTPRequest): request of invoker of http-request

        """
        pass
