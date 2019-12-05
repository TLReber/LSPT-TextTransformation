#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file supplies helper functions to handle transformation of input data to 
output. The Worker uses these tools to parse its transformations
"""

import re


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
    if(executing == False):
        return ""
    if(soup_instance.title == None):
        return ""
    if(soup_instance.title.string == None):
        return ""
    return soup_instance.title.string;


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
    #remove style and script tags
    text = ""
    if soup_instance.html != None:
        for styletag in soup_instance.html.find_all("style"):
            styletag.clear()
        for scripttag in soup_instance.find_all("script"):
            scripttag.clear()
    
        text = soup_instance.text
    else:
        text = soup_instance.__str__()
    text = text.lower()
    #remove non alpha characters
    stripped_words = re.findall("[a-z]+(?:'[a-z]+)?", text)

    return_text = ""
    for word in stripped_words:
        if word not in stop_word_list:
            if return_text != "":
                return_text += " "
            return_text += word
    return return_text


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
    #remove style and script tags
    text = ""
    if soup_instance.html != None:
        for styletag in soup_instance.html.find_all("style"):
            styletag.clear()
        for scripttag in soup_instance.find_all("script"):
            scripttag.clear()
    
        text = soup_instance.text
    else:
        text = soup_instance.__str__()
    text = text.lower()
    #remove non alpha characters
    stripped_words = re.findall("[a-z]+(?:'[a-z]+)?", text)
    return_dict = dict()

    for ngram_size in n:
        #make a sub-dict for each size n
        return_dict[ngram_size] = dict()
        for index in range(len(stripped_words) - (ngram_size - 1)):
            accepted_ngram = True
            ngram_key = ""
            for ngram_index in range(ngram_size):
                if stripped_words[index + ngram_index] in stop_word_list:
                    accepted_ngram = False
                    break
                else:
                    if(ngram_index != 0):
                        ngram_key += " "
                    ngram_key += stripped_words[index + ngram_index]
                    
            if accepted_ngram:
                if ngram_key not in return_dict[ngram_size].keys():
                    return_dict[ngram_size][ngram_key] = list()
                return_dict[ngram_size][ngram_key].append(index)
    return return_dict
