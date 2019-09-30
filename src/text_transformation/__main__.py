#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file that houses all the entry points, the default script is run_server which
spins up a server to take in api requests
"""
import sys
from text_transformation.server import Server

def run_node():
    print(sys.argv[1:])
    server = Server()
    server.run()


if __name__ == "__main__":
    run_node()
