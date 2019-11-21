#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Transformer:
    """
    Handles transformation of input data to output. Changes based on
    type of string given during initialization regular expression specified.
    Follows a state design pattern: wraps functions defined below to accomplish 
    this

    Attributes:
        transformations(list): list of tuples where first item is the string
            expression of a transformation and the value is a function. This 
            attribute is a class attribute
        func((*args, **kwargs)->object): function that was chosen based on
            input type

    Raises:
        ValueError: function not found from name provided

    Examples:
        titleTransform = Transformer("title")
        titleTransform(true, soup instance with "<title>hello</title>") #returns "hello"
        ngramTransform = Transformer("ngrams")
        ngramTransform([] ,[1, 2, 4], soup instance with "hello hello world") #returns 
            {1: {"hello": [0, 1], "world": [2]}, 2: {"hello hello": [0], "hello world": [1]}, 4: {}}
    """

    def __init__(
        self, state: str,
    ):
        """
        """
        pass


    def __call__(self, *args, **kwargs):
        pass

stop_word_list = []

def title(executing: bool, soup_instance = None):
    """
    Takes a soup instance a returns the title

    Args:
        executing(bool): If true, this function returns the title, otherwise it returns nothing
        soup_instance: An instance of BeautifulSoup that contains the text to transform

    Returns:
        (string): A string that contains the title or None

    """
    pass

def stripped(stop_word_list = [], soup_instance = None):
    """
    Takes a soup instance and filters out html tags and stop words and returns the resulting text

    Args:
        stop_word_list(list): A list of stop words to be filtered
        soup_instance: An instance of BeautifulSoup that contains the text to transform

    Returns:
        (string): A string that does not contain html tags or stop words

    """
    pass

def ngrams(stop_word_list = [], n = [], soup_instance = None):
    """
    Takes a soup instance, a list of n, and a list of stop words and returns all resulting ngrams without
    stop words

    Args:
        stop_word_list(list): A list of stop words to be filtered
        n(list): A list containing The amount of words in each gram (i.e. 2-gram or 5-gram)
        soup_instance: An instance of BeautifulSoup that contains the text to transform

    Returns:
        (dict): A dictionary where the keys are each n and the values are their own dictionary where the keys
        is each ngram while the values are a list of their occurrences
    """
    pass





