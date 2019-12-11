import requests
import json
import time
import threading
import sys


def test_empty_json(address):
    address = f"http://{address}/transform"
    print(address)
    data = {
        "type": "hmtl",
        "data": "",
        "transformations": { }
    }
    print(requests.post(address, json=data).json())

    
def test_simple_json(address):
    address = f"http://{address}/transform"
    print(address)
    data = {
        "type": "hmtl",
        "data": "<html><p>hello hello world this is some test, go and parse this!</p></hmtl>",
        "transformations": { 
            "stripped": True,
            "grams": [1, 2, 3],
            "title": True
        }
    }
    print(requests.post(address, json=data).json())

def test1(addr):

    print("test 1 running, nothing should be printed from this test.\n")
    # the port number will be replaced with the actual port number that
    # the text transformation server is using
    addr = f"http://{addr}/transform"

    # the json that goes with the request
    data = {
        "type": "html",
        "data": "<html><p> hello hello world this is some test, go and parse this! </p></html>",
        "transformations": {
            "stripped": True,
            "grams": [1,2,3],
            "Title": False
        }
    }
    
    data = json.dumps(data)
    
    # making the request
    respond = requests.post(addr, data=data)
    
    print("HTTP response status code: " + str(respond.status_code))
    
    # converting the data we receive in response to json form
    
    respond_json = respond.json()
    
    # making sure we have the correct results
    try:
    
        assert (
            respond_json["stripped"]
            == "hello hello world some test go parse"
        )
    
    except:
        print("stripped words do not match (test 1)")
    
    grams = {}
    grams["1"] = {}
    grams["2"] = {}
    grams["3"] = {}
    
    grams["1"]["hello"] = [0, 1]
    grams["1"]["world"] = [2]
    grams["1"]["some"] = [5]
    grams["1"]["test"] = [6]
    grams["1"]["go"] = [7]
    grams["1"]["parse"] = [9]
    
    grams["2"]["hello hello"] = [0]
    grams["2"]["hello world"] = [1]
    grams["2"]["some test"] = [5]
    grams["2"]["test go"] = [6]
    
    grams["3"]["hello hello world"] = [0]
    grams["3"]["some test go"] = [5]
    
    grams = json.dumps(grams)
    grams = json.loads(grams)
    
    print(respond_json["stripped"])
    print(respond_json["grams"]["1"])
    #why the fuck is grams a string???
    
    assert respond_json["grams"]['1'] == grams['1'], "words do not match (test 1)"
    assert respond_json["grams"]['1'] == grams['1'], "bigrams do not match (test 1)"
    assert respond_json["grams"]['1'] == grams['1'], "trigrams go not match (test 1)"
    
    print("\n")


def test2(addr):

    print(
        "test 2 running, this should print a 400 error, indicating that the parameters are invalid\n"
    )
    # the port number will be replaced with the actual port number that the 
    # text transformation server is using
    addr = f"http://{addr}/transform"

    # the json that goes with the request
    data = {
        "type": "html",
        "data": "<p>hello hello world this is some test, go and parse this!<\p>",
        "transformations": {
            "stripped": True,
            "grams": [1,2,3],
            "Title": False,
            "some random parameter": False
        }
    }
    
    data = json.dumps(data)
    
    respond = requests.post(addr, data=data)
    
    # should print the error code we're getting from the server
    print("HTTP response status code: " + str(respond.status_code) + "\n")


def test3(addr):

    print("test 3 running, nothing should be printed from this test.\n")

    # the port number will be replaced with the actual port number that the 
    # text transformation server is using
    addr = f"http://{addr}/transform"

    # the json that goes with the request
    data = {
        "type": "html",
        "data": "",
        "transformations": {
            "stripped": True,
            "grams": [1,2,3],
            "Title": False
        }
    }
    
    data = json.dumps(data)
    
    # making the request
    respond = requests.post(addr, data=data)
    
    # converting data we received in response to json
    respond_json = respond.json()
    
    
    # make sure we're getting the correct response
    assert respond_json["stripped"] == ""

    assert respond_json["grams"]["1"] == {}, "words do not match (test 1)"

    assert respond_json["grams"]["2"] == {}, "bigrams do not match (test 1)"

    assert respond_json["grams"]["3"] == {}, "trigrams go not match (test 1)"


def test4(addr):

    print(
        "test 4 running, the time used to process this request will be printed.\n"
    )
    
    

    # the port number will be replaced with the actual port number that the 
    # text transformation server is using
    addr = f"http://{addr}/transform"

    # load the json we're using
    data = json.load(open("api_tests/lots_of_data.json"), strict = False)
    
    # the time the request is made
    start = time.time()
    
    # make the request
    respond = requests.post(addr, data=data)
        
    # the time we receive response and convert the response to json
    end = time.time()
    
    # print the time used for the server to handle the request
    print(end - start)
    print("\n")

    # don't care about the actual response

def test_submitty_html():
    print("testing with submitty.json")
    
    # the port number will be replaced with the actual port number that the
    # text transformation server is using
    addr = "http://127.0.0.1:" + str(sys.argv[1]) + "/transform"

    # load the json we'll be using
    data = json.load(open("api_tests/submitty.json"), strict = False)
    # make the request
    
    print(data)
    
    respond = requests.post(addr, data=data)
    
    print("HTTP response status code: " + str(respond.status_code) + "\n")
    
    respond_json = respond.json()
    
    print(respond_json)
    
    # check that the statistics are correct
    # we've ran the data through hw2 so the statistics should be correct
    assert len(respond_json["stripped"]) == 539, "total word count incorrect"
    
    assert len(respond_json["grams"]["1"]) == 309, "unique word count incorrect"
    
    assert len(respond_json["grams"]["2"]) == 369, "unique bigram count incorrect"
    
    assert len(respond_json["grams"]["3"]) == 341, "unique trigram count incorrect"
    
def test_ecse_1010_html(addr):
    print("testing with ECSE_1010.json")
    
    # the port number will be replaced with the actual port number that the
    # text transformation server is using
    addr = f"http://{addr}/transform"

    # load the json we'll be using
    data = json.load(open("api_test/ECSE_1010.json"))
    
    # make the request
    respond = requests.post(addr, data=data)
    
    respond_json = respond.json()
    
    # check that the statistics are correct
    # we've ran the data through hw2 so the statistics should be correct
    assert len(respond_json["stripped"]) == 3603, "total word count incorrect"
    
    assert len(respond_json["grams"]["1"]) == 908, "unique word count incorrect"
    
    assert len(respond_json["grams"]["2"]) == 1487, "unique bigram count incorrect"
    
    assert len(respond_json["grams"]["3"]) == 1373, "unique trigram count incorrect"
    
def test_wikipedia_html():
    print("testing with wikipedia.json")
    
    # the port number will be replaced with the actual port number that the
    # text transformation server is using
    addr = "http://127.0.0.1:" + str(sys.argv[1]) + "/transform"

    # load the json we'll be using
    data = json.load(open("api_test/wikipedia.json"))
    
    # make the request
    respond = requests.post(addr, data=data)
    
    respond_json = request.json()
    
    # check that the statistics are correct
    # we've ran the data through hw2 so the statistics should be correct
    assert len(respond_json["stripped"]) == 34070, "total word count incorrect"
    
    assert len(respond_json["grams"]["1"]) == 5695, "unique word count incorrect"
    
    assert len(respond_json["grams"]["2"]) == 12118, "unique bigram count incorrect"
    
    assert len(respond_json["grams"]["3"]) == 12617, "unique trigram count incorrect"
    
def test_grpc_html():
    print("testing with grpc.json")
    
    # the port number will be replaced with the actual port number that the
    # text transformation server is using
    addr = "http://127.0.0.1:" + str(sys.argv[1]) + "/transform"

    # load the json we'll be using
    data = json.load(open("api_test/wikipedia.json"))
    
    # make the request
    respond = requests.post(addr, data=data)
    
    respond_json = request.json()
    
    # check that the statistics are correct
    # we've ran the data through hw2 so the statistics should be correct
    assert len(respond_json["stripped"]) == 7091, "total word count incorrect"
    
    assert len(respond_json["grams"]["1"]) == 715, "unique word count incorrect"
    
    assert len(respond_json["grams"]["2"]) == 1543, "unique bigram count incorrect"
    
    assert len(respond_json["grams"]["3"]) == 1497, "unique trigram count incorrect"

def test_diodes_html():
    print("testing with diodes.json")
    
    # the port number will be replaced with the actual port number that the
    # text transformation server is using
    addr = "http://127.0.0.1:" + str(sys.argv[1]) + "/transform"

    # load the json we'll be using
    data = json.load(open("api_test/diodes.json"))
    
    # make the request
    respond = requests.post(addr, data=data)
    
    respond_json = request.json()
    
    # check that the statistics are correct
    # we've ran the data through hw2 so the statistics should be correct
    assert len(respond_json["stripped"]) == 21740, "total word count incorrect"
    
    assert len(respond_json["grams"]["1"]) == 2099, "unique word count incorrect"
    
    assert len(respond_json["grams"]["2"]) == 4778, "unique bigram count incorrect"
    
    assert len(respond_json["grams"]["3"]) == 6945, "unique trigram count incorrect"

def test_non_json_put_request(addr):
    print("testing with non-json data")
    
    # the port number will be replaced with the actual port number that the
    # text transformation server is using
    addr = f"http://{addr}/transform"

    # we should be sending json instead of this text in the request,
    # so we should be receiving some error code from the server since this
    # request doesn't make sense
    text = "this is some random text and this request doesn't make any sense"

    # make the request
    respond = requests.post(addr, data = text)
    
    #see what error(s) we get from the server
   
    
    print("HTTP response status code: " + str(respond.status_code))

if __name__ == "__main__":
    test1(sys.argv[1])  # successful request
    test2(sys.argv[1])  # invalid parameters
    test3(sys.argv[1])  # no data
    test4(sys.argv[1])  # lots of data (1.2MB)
    
    #testing with different (known) data
    
    # apparently the results are affected by the CSS styling code - HW2 couldn't
    # handle (ignore) text between CSS <style> tags
    # the impact of CSS on the results are unknown
    test_submitty_html(sys.argv[1])
    #test_ecse_1010_html()
    #test_wikipedia_html()
    #test_grpc_html()
    #test_diodes_html()
    
    
    #test_empty_json(sys.argv[1])
    #test_simple_json(sys.argv[1])
    test_non_json_put_request(sys.argv[1]) # request that doesn't make sense


# post and verify results, use assert statements
