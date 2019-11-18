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

    Example:
        titleTransform = Transformer("title")
        titleTransform(true, soup instance with "<title>hello</title>") #returns "hello"
        ngramTransform = Transformer("ngrams")
        ngramTransform([1, 2, 4], soup instance with "ab ce ce") #returns {1: [[1, 0, "ab"], [2, 1, 2, "ce"]], 2: [[1, 0, "ab ce"], [1, 1, "ce ce"]], 4: []}
    """

    def __init__(
        self, state: str,
    ):
        """
        """
        pass


    def __call__(self, *args, **kwargs):
        pass

def title(text):
    pass

def strip(text):
    pass

def ngrams(n, text):
    pass





