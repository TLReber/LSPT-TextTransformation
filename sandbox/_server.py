#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from aiohttp import web
import asyncio

from text_transformation.transformer import Transformer


class Server:
    def __init__(self):
        app = web.Application()

        # adding current routes
        routes = [
            web.post("/transform_text", self.transform_text)
        ]
        app.add_routes(routes)

        self.app = app

    def run(self):
        t = Transformer()
        web.run_app(self.app)

    async def transform_text(self, request):
        print(request)
        return web.Response(text="Hello, world")
