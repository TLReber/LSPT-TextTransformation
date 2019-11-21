#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file supplies helper functions to handle transformation of input data to 
output. The Worker uses these tools to parse its transformations
"""

stop_word_list = []


def title(executing: bool, soup_instance=None):
    """
    Takes a soup instance a returns the title. If there is no title, it will then check h1, then
    h2, h3, h4, h5, h6, and the p tag in order. This function will only return a title of a constant
    size

    Args:
        executing(bool): If true, this function returns the title, otherwise 
            it returns nothing
        soup_instance: An instance of BeautifulSoup that contains the text to 
            transform

    Returns:
        (string): A string that contains the title or ""

    """
    pass


def stripped(stop_word_list=[], soup_instance=None):
    """
    Takes a soup instance and filters out html tags and stop words and returns 
    the resulting text in all lower case

    Args:
        stop_word_list(list): A list of stop words to be filtered
        soup_instance: An instance of BeautifulSoup that contains the text to 
            transform

    Returns:
        (string): A string that does not contain html tags or stop words

    """
    pass


def ngrams(stop_word_list=[], n=[], soup_instance=None):
    """
    Takes a soup instance, a list of n, and a list of stop words and returns 
    all resulting ngrams without stop words

    Args:
        stop_word_list(list): A list of stop words to be filtered
        n(list): A list containing The amount of words in each gram 
            (i.e. 2-gram or 5-gram)
        soup_instance: An instance of BeautifulSoup that contains the text to 
            transform

    Returns:
        (dict): A dictionary where the keys are each n and the values are 
            their own dictionary where the keys is each ngram while the values 
            are a list of their occurrences
    """
    pass
