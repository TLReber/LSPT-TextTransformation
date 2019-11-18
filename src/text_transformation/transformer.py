#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Transformer:
    """
    Handles transformation of input data to output. Changes based on
    type of string given during initialization regular expression specified.
    Follows a state design pattern: wraps functions defined below to accomplish 
    this

    Attributes:
        transformations(list): list of tuples where first item is the regular
            expression of a transformation and the value is a function. This 
            attribute is a class attribute
        func((*args, **kwargs)->object): function that was chosen based on
            input type

    Raises:
        ValueError: function not found from name provided
    """

    def __init__(
        self, state: str,
    ):
        """
        """
        pass

    def __call__(self, *args, **kwargs):
        pass
