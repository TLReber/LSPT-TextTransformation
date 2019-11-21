import requests
import json
import time
import threading

def test1():
    
    print("test 1 running, nothing should be printed from this test.\n")
    
    addr = "http://127.0.0.1:8000" #the port number will be replaced with the actual port number that the text transformation server is using
    
    data = {"$type":"html",
            "$data":"<p>hello hello world this is some test, go and parse this!<\p>",
            "$transformations":["stripped", "1-gram", "2-gram", "3-gram", "title"]}
    
    respond = requests.put(addr, json=data)
    
    respond_json = respond.json()
    
    assert respond_json['stripped'] == "hello hello world this is some test go and parse this", "stripped words do not match (test 1)"
    
    words = {"$hello":[0, 1], "$world":[2], "$this":[3,10], "$is":[4], "$some":[5], "$test":[6], "$go":[7], "$and":[8], "$parse":[9]}
    assert respond_json['1-gram'] == words, "words do not match (test 1)"
    
    bigrams = {"$hello hello":[0], "$hello world":[1], "$world this":[2], "$this is":[3], "$is some":[4], "$some test":[5], "$test go":[6], "$go and":[7], "$and parse": [8], "$parse this":[9]}
    assert respond_json['2-gram'] == bigrams, "bigrams do not match (test 1)"
    
    trigrams = {"$hello hello world":[0], "$hello world this":[1], "$world this is": [2], "$this is some": [3], "$is some test":[4], "$some test go":[5], "$test go and":[6], "$go and parse":[7], "$and parse it":[8]}
    assert respond_json['3-gram'] == trigrams, "trigrams go not match (test 1)"

def test2():

    print("test 2 running, this should print a 400 error, indicating that the parameters are invalid\n")
    addr = "http://127.0.0.1:8001" #the port number will be replaced with the actual port number that the text transformation server is using
    
    data = {"$type":"html",
            "$data":"<p>hello hello world this is some test, go and parse this!<\p>",
            "$transformations":["invalid-param", "1-gram", "2-gram", "3-gram", "title"]}
    
    respond = requests.put(addr, json=data)
    
    respond.raise_for_status() #this is return and print some error

def test3():
    
    print("test3 running, nothing should be printed from this test.\n")

    addr = "http://127.0.0.1:8000" #the port number will be replaced with the actual port number that the text transformation server is using
    
    data = {"$type":"html",
            "$data":"",
            "$transformations":["stripped", "1-gram", "2-gram", "3-gram", "title"]}
    
    respond = requests.put(addr, json=data)
    
    respond_json = respond.json()
    
    assert respond_json['stripped'] == ""
    
    words = {}
    assert respond_json['1-gram'] == words, "words do not match (test 1)"
    
    bigrams = {}
    assert respond_json['2-gram'] == bigrams, "bigrams do not match (test 1)"
    
    trigrams = {}
    assert respond_json['3-gram'] == trigrams, "trigrams go not match (test 1)"

def test4():

    print("test4 running, the time used to process this request will be printed.\n")
    
    start = time.time()
    
    addr = "http://127.0.0.1:8000" #the port number will be replaced with the actual port number that the text transformation server is using
    
    data = json.load(open("api_tests/lots_of_data.json"))
    
    respond = requests.put(addr, json=data)
    
    respond_json = respond.json()
    
    end = time.time()
    
    print(end - start)
    print("\n")
    

if __name__ == "__main__":
    test1() #successful request
    test2() #invalid parameters
    test3() #no data
    test4() #lots of data (1.2MB)
    

    
    
# post and verify results, use assert statements


