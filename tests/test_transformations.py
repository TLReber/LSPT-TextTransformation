#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file tests all the available transformations in the transformations.py file
"""

import pytest
from bs4 import BeautifulSoup
from text_transformation.transformations import title, stripped, ngrams

stop_words_list = ["the", "a"]

text1 = "hello hello world"
text2 = "hello hello hello"
text3 = "the"
text4 = "the the the"
text5 = "a"
text6 = '<script>console.log("Hello")</script>'

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
html5 = "<html><head><title></title></head><body>the</body></html>"
html6 = """
	<html>
	<head>
	<style>
	p {
  		color: red;
  		text-align: center;
	} 
	</style>
	</head>
	<body>

	<p>Hello World!</p>
	<p>These paragraphs are styled with CSS.</p>

	</body>
	</html>
"""

html7 = """
	<html>
	<head>
	<script>
		console.log("Hello World")
	</script>
	</head>
	<body>

	<p>Hello World!</p>
	<p>These paragraphs are styled with CSS.</p>

	</body>
	</html>
"""

html8 = """
	<html>
	<head>
	<style>
	p {
  		color: red;
  		text-align: center;
	} 
	</style>
	<style>
	p {
  		color: blue;
  		text-align: center;
	} 
	</style>
	</head>
	<body>

	<p>Hello World!</p>
	<p>These paragraphs are styled with CSS.</p>

	</body>
	</html>
"""

html9 = """
	<html>
	<head>
	<script>
		console.log("Hello World")
	</script>
	<script>
		console.log("Goodbye World")
	</script>
	</head>
	<body>

	<p>Hello World!</p>
	<p>These paragraphs are styled with CSS.</p>

	</body>
	</html>
"""


def test_transformer_title():
    t = title
    # titles for all non html documents should be ""
    soup = BeautifulSoup(text1, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(text2, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(text3, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(text4, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(text5, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(text6, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    # The title is not stripped or set to lowercase
    soup = BeautifulSoup(html1, "html.parser")
    assert t(True, soup) == "The Dormouse's story"
    assert t(False, soup) == ""
    soup = BeautifulSoup(html2, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(html3, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(html4, "html.parser")
    assert t(True, soup) == "the"
    assert t(False, soup) == ""
    soup = BeautifulSoup(html5, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(html6, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(html7, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(html8, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""
    soup = BeautifulSoup(html9, "html.parser")
    assert t(True, soup) == ""
    assert t(False, soup) == ""


def test_transformer_stripped():
    t = stripped
    soup = BeautifulSoup(text1, "html.parser")
    assert t(True, stop_words_list, soup) == "hello hello world"
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(text2, "html.parser")
    assert t(True, stop_words_list, soup) == "hello hello hello"
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(text3, "html.parser")
    assert t(True, stop_words_list, soup) == ""
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(text4, "html.parser")
    assert t(True, stop_words_list, soup) == ""
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(text5, "html.parser")
    assert t(True, stop_words_list, soup) == ""
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(text6, "html.parser")
    assert t(True, stop_words_list, soup) == "script console log hello script"
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html1, "html.parser")
    assert (
        t(True, stop_words_list, soup)
        == "dormouse's story dormouse's story once upon time"
    )
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html2, "html.parser")
    assert t(True, stop_words_list, soup) == "words words words"
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html3, "html.parser")
    assert t(True, stop_words_list, soup) == ""
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html4, "html.parser")
    assert t(True, stop_words_list, soup) == ""
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html5, "html.parser")
    assert t(True, stop_words_list, soup) == ""
    assert t(False, stop_words_list, soup) == ""
    # should remove contents of style or script tags
    soup = BeautifulSoup(html6, "html.parser")
    assert (
        t(True, stop_words_list, soup)
        == "hello world these paragraphs are styled with css"
    )
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html7, "html.parser")
    assert (
        t(True, stop_words_list, soup)
        == "hello world these paragraphs are styled with css"
    )
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html8, "html.parser")
    assert (
        t(True, stop_words_list, soup)
        == "hello world these paragraphs are styled with css"
    )
    assert t(False, stop_words_list, soup) == ""
    soup = BeautifulSoup(html9, "html.parser")
    assert (
        t(True, stop_words_list, soup)
        == "hello world these paragraphs are styled with css"
    )
    assert t(False, stop_words_list, soup) == ""


def test_transformer_ngrams():
    t = ngrams
    soup = BeautifulSoup(text1, "html.parser")
    assert t([1, 2, 3, 4], stop_words_list, soup) == {
        1: {"hello": [0, 1], "world": [2]},
        2: {"hello hello": [0], "hello world": [1]},
        3: {"hello hello world": [0]},
        4: {},
    }
    soup = BeautifulSoup(text2, "html.parser")
    assert t([1, 2, 3, 4], stop_words_list, soup) == {
        1: {"hello": [0, 1, 2]},
        2: {"hello hello": [0, 1]},
        3: {"hello hello hello": [0]},
        4: {},
    }
    soup = BeautifulSoup(text3, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(text4, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(text5, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(text6, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {
        1: {"script": [0, 4], "console": [1], "log": [2], "hello": [3]},
        2: {
            "script console": [0],
            "console log": [1],
            "log hello": [2],
            "hello script": [3],
        },
        3: {
            "script console log": [0],
            "console log hello": [1],
            "log hello script": [2],
        },
    }
    # script console log hello script
    soup = BeautifulSoup(html1, "html.parser")
    assert t([1, 2, 3, 4], stop_words_list, soup) == {
        1: {
            "dormouse's": [1, 4],
            "story": [2, 5],
            "once": [6],
            "upon": [7],
            "time": [9],
        },
        2: {"dormouse's story": [1, 4], "story once": [5], "once upon": [6]},
        3: {"dormouse's story once": [4], "story once upon": [5]},
        4: {"dormouse's story once upon": [4]},
    }
    soup = BeautifulSoup(html2, "html.parser")
    assert t([1, 2, 3, 4], stop_words_list, soup) == {
        1: {"words": [0, 1, 2]},
        2: {"words words": [0, 1]},
        3: {"words words words": [0]},
        4: {},
    }
    soup = BeautifulSoup(html3, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(html4, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(html5, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {1: {}, 2: {}, 3: {}}
    soup = BeautifulSoup(html6, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {
        1: {
            "hello": [0],
            "world": [1],
            "these": [2],
            "paragraphs": [3],
            "are": [4],
            "styled": [5],
            "with": [6],
            "css": [7],
        },
        2: {
            "hello world": [0],
            "world these": [1],
            "these paragraphs": [2],
            "paragraphs are": [3],
            "are styled": [4],
            "styled with": [5],
            "with css": [6],
        },
        3: {
            "hello world these": [0],
            "world these paragraphs": [1],
            "these paragraphs are": [2],
            "paragraphs are styled": [3],
            "are styled with": [4],
            "styled with css": [5],
        },
    }
    soup = BeautifulSoup(html7, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {
        1: {
            "hello": [0],
            "world": [1],
            "these": [2],
            "paragraphs": [3],
            "are": [4],
            "styled": [5],
            "with": [6],
            "css": [7],
        },
        2: {
            "hello world": [0],
            "world these": [1],
            "these paragraphs": [2],
            "paragraphs are": [3],
            "are styled": [4],
            "styled with": [5],
            "with css": [6],
        },
        3: {
            "hello world these": [0],
            "world these paragraphs": [1],
            "these paragraphs are": [2],
            "paragraphs are styled": [3],
            "are styled with": [4],
            "styled with css": [5],
        },
    }
    soup = BeautifulSoup(html8, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {
        1: {
            "hello": [0],
            "world": [1],
            "these": [2],
            "paragraphs": [3],
            "are": [4],
            "styled": [5],
            "with": [6],
            "css": [7],
        },
        2: {
            "hello world": [0],
            "world these": [1],
            "these paragraphs": [2],
            "paragraphs are": [3],
            "are styled": [4],
            "styled with": [5],
            "with css": [6],
        },
        3: {
            "hello world these": [0],
            "world these paragraphs": [1],
            "these paragraphs are": [2],
            "paragraphs are styled": [3],
            "are styled with": [4],
            "styled with css": [5],
        },
    }
    soup = BeautifulSoup(html9, "html.parser")
    assert t([1, 2, 3], stop_words_list, soup) == {
        1: {
            "hello": [0],
            "world": [1],
            "these": [2],
            "paragraphs": [3],
            "are": [4],
            "styled": [5],
            "with": [6],
            "css": [7],
        },
        2: {
            "hello world": [0],
            "world these": [1],
            "these paragraphs": [2],
            "paragraphs are": [3],
            "are styled": [4],
            "styled with": [5],
            "with css": [6],
        },
        3: {
            "hello world these": [0],
            "world these paragraphs": [1],
            "these paragraphs are": [2],
            "paragraphs are styled": [3],
            "are styled with": [4],
            "styled with css": [5],
        },
    }
