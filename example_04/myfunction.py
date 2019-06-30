"""myfunction.py"""

import requests

def myfunction(numbers):
    """Adds up all ints in numbers and returns the result"""
    return sum(numbers)

def awesomefunction():
    """Returns stuff!"""
    r = requests.get('http://localhost/', json={})
    return r.json()
