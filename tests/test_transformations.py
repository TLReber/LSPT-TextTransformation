#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests all the available transformations in the transformations.py fil
"""

import pytest
from bs4 import BeautifulSoup
from text_transformation.transformations import title, stripped, ngrams

__author__ = "gregjhansell97"
__copyright__ = "gregjhansell97"
__license__ = "mit"

stop_words_list = ["the", "a"]

text1 = "hello hello world"
text2 = "hello hello hello"
text3 = "the"
text4 = "the the the"
html1 = """
	<html><head><title>The Dormouse's story</title></head>
	<body>
	<p class="title"><b>The Dormouse's story</b></p>

	<p class="story">Once upon a time
	</p>

	<p class="story">...</p>
"""

html2 = (
    "<html><head><title></title></head><body>words words words</body></html>"
)
html3 = "<html></html>"
html4 = "<html><head><title>the</title></head><body></body></html>"
html4 = "<html><head><title></title></head><body>the</body></html>"


def test_transformer_title():
    t = title
    soup = BeautifulSoup(text1, "html.parser")
    assert t(True, soup) == None
    assert t(False, soup) == None
    soup = BeautifulSoup(text2, "html.parser")
    assert t(True, soup) == None
    assert t(False, soup) == None
    soup = BeautifulSoup(text3, "html.parser")
    assert t(True, soup) == None
    assert t(False, soup) == None
    soup = BeautifulSoup(text4, "html.parser")
    assert t(True, soup) == None
    assert t(False, soup) == None
    soup = BeautifulSoup(html1, "html.parser")
    assert t(True, soup) == "The Dormouse's story"
    assert t(False, soup) == None
    soup = BeautifulSoup(html2, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == None
    soup = BeautifulSoup(html3, "html.parser")
    assert t(True, soup) == None
    assert t(False, soup) == None
    soup = BeautifulSoup(html4, "html.parser")
    assert t(True, soup) == "the"
    assert t(False, soup) == None
    soup = BeautifulSoup(html5, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == None


def test_transformer_stripped():
    t = stripped
    soup = BeautifulSoup(text1, "html.parser")
    assert t(stop_words_list, soup) == "hello hello world"
    soup = BeautifulSoup(text2, "html.parser")
    assert t(stop_words_list, soup) == "hello hello hello"
    soup = BeautifulSoup(text3, "html.parser")
    assert t(stop_words_list, soup) == ""
    soup = BeautifulSoup(text4, "html.parser")
    assert t(stop_words_list, soup) == ""
    soup = BeautifulSoup(html1, "html.parser")
    assert (
        t(stop_words_list, soup)
        == "dormouse's story dormouse's story once upon time"
    )
    soup = BeautifulSoup(html2, "html.parser")
    assert t(stop_words_list, soup) == "words words words"
    soup = BeautifulSoup(html3, "html.parser")
    assert t(stop_words_list, soup) == ""
    soup = BeautifulSoup(html4, "html.parser")
    assert t(stop_words_list, soup) == ""
    soup = BeautifulSoup(html5, "html.parser")
    assert t(stop_words_list, soup) == ""


def test_transformer_ngrams():
    t = ngrams
    soup = BeautifulSoup(text1, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {
        1: {"hello": [0, 1], "world": [2]},
        2: {"hello hello": [0], "hello world": [1]},
        3: {"hello hello world": [0]},
    }
    soup = BeautifulSoup(text2, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {
        1: {"hello": [0, 1, 2]},
        2: {"hello hello": [0, 1]},
        3: {"hello hello hello": [0]},
    }
    soup = BeautifulSoup(text3, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(text4, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(html1, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {
        1: {
            "dormouse's": [1, 4],
            "story": [2, 5],
            "once": [6],
            "upon": [7],
            "time": [9],
        },
        2: {"dormouse's story": [1, 4], "story once": [5], "once upon": [6]},
        3: {"dormouse's story once": [5], "story once upon": [6]},
    }
    soup = BeautifulSoup(html2, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {
        1: {"words": [0, 1, 2]},
        2: {"words words": [0, 1]},
        3: {"words words words": [0]},
    }
    soup = BeautifulSoup(html3, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(html4, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(html5, "html.parser")
    assert t(stop_words_list, [1, 2, 3], soup) == {1: {}, 2: {}, 3: {}}
