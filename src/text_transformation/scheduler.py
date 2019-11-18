#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Scheduler:
    """
    Front-facing server that handles api requests and delegates work to workers.
    Uses asyncio to handle post requests

    API: 
        /transform(POST): takes in a description of the data, the
        applied transformations to apply and targets to post the
        transformations to. If there are no targets, then the transformation
        is returned back to "POSTER" of input

    Attributes:
        app(web.Application): helper tool to setup http request system
        name(str): string identifier unique across processes
        results(dict): key of unique work request id, value of future
        request_id(int): used to assign unique ids for results
        listen_thread(Thread): runs self.listen in background to make 
            self.results awaitable
        
    """

    def __init__(
        self, name: str,
    ):
        pass

    def __del__(self):
        pass

    def stop(self):
        """
        Ends self.listen_thread
        """
        pass

    async def transform(self, request):
        """
        HTTP request is routed here, what is expected of request is:
        {
            type: str,
            data: str,
            transformed: [str],
            targets: [str]
        }

        Args:
            request(HTTPRequest): request of invoker of http-request
        """
        pass
