import requests
from requests.adapters import HTTPAdapter

__author__ = 'Miguel'


def get_json(uri, params):
    """
    Returns a JSON document given an API's URI
    :param uri:
    :param params:
    :return json_response:
    """
    s = requests.Session()
    s.mount(uri, HTTPAdapter(max_retries=10))
    json_response = requests.get(uri, params=params).json()
    return json_response