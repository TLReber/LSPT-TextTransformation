===================
Text Transformation
===================


Server that parses through raw document data to determine meaningful statistics 
to be used in ranking and querying.

Description
===========

A longer description of your project goes here...

Installation
============
- Using python 3.7 though 3.6 should work

For linux:

.. code-block:: bash

    python -m venv .tt-env
    source .tt-env/bin/activate
    pip install -e .

Running Unit Testing
====================

After installing:

.. code-block:: bash

    python setup.py test

Running API Testing
====================

After installing:

.. code-block:: bash

    python api_test

Running A Worker
=================

After installing:

.. code-block:: bash

    text-trans-worker

Running A Scheduler
===================

After installing:

.. code-block:: bash

    text-trans-scheduler

Connecting to the Server
========================
.. code-block:: bash
    
    ssh {RCS-ID}@lspt-text1.cs.rpi.edu
    sudo bash
    cd /LSPT-TextTransformation

Note
====

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
