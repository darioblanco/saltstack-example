# -*- coding: utf-8 -*-
"""
Test beacon to emit nginx connection status.
"""

import os
import sys

import requests

# Workaround for adding nginx_connections to the PYTHONPATH
PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(PATH, os.pardir, 'roots', 'salt', '_beacons'))

from nginx_connections import beacon, validate


def test_valid_config():
    """Verify a correct config object."""
    config = {'protocol': 'http', 'port': 80, 'host': 'localhost'}
    assert validate(config) == (True, 'Valid beacon configuration.')


def test_config_not_dict():
    """Reject a config that is not a dict."""
    config = ['list', 'of', 'things']
    assert validate(config) == (False, 'Configuration for nginx_connections '
                                       'beacon must be a dictionary.')


def test_config_wrong_protocol():
    """Reject a config a protocol other than http or https."""
    config = {'protocol': 'sftp', 'port': 80, 'host': 'localhost'}
    assert validate(config) == (False, "Protocol configuration for "
                                       "nginx_connections should be in "
                                       "['http', 'https'].")


def test_config_port_not_a_number():
    """Reject a config with a port that is not a number."""
    config = {'protocol': 'http', 'port': 'foo', 'host': 'localhost'}
    assert validate(config) == (
        False, 'Port configuration for nginx_connections is not a number.')


def test_config_port_wrong_number():
    """Reject a config with a port out of the valid range."""
    for port in [0, 70000]:
        config = {'protocol': 'http', 'port': port, 'host': 'localhost'}
        assert validate(config) == (
            False, 'Port configuration for nginx_connection '
                   'is not a valid port number.')


def test_config_host_wrong():
    """Reject a config with a host that cannot be resolved."""
    config = {'protocol': 'http', 'port': 80, 'host': 'foohost'}
    assert validate(config) == (
        False, 'Host configuration for nginx_connection cannot be resolved.')


class Response(requests.Response):
    """Mock class for requests response."""

    def __init__(self):
        self._text = None
        self._status_code = 200

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value):
        self._status_code = value


def test_beacon_nginx_correct_status_message(monkeypatch):
    """Verify statistics from a correct nginx status response."""
    config = {'protocol': 'http', 'port': 80, 'host': 'localhost'}
    mocked_response = Response()
    mocked_response.text = ('Active connections: 3 \n'
                            'server accepts handled requests\n'
                            ' 97 97 96 \n'
                            'Reading: 2 Writing: 1 Waiting: 0 ')
    monkeypatch.setattr(requests, 'get', lambda x: mocked_response)
    assert beacon(config) == [
        {'accepted': 97, 'handled': 97, 'open': 3, 'reading': 2,
         'requests': 96, 'requests_per_conn': 0, 'waiting': 0, 'writing': 1}
    ]


def test_beacon_nginx_wrong_status_message(monkeypatch):
    """Avoid returning statistics for an unexpected nginx response body."""
    config = {'protocol': 'http', 'port': 80, 'host': 'localhost'}
    mocked_response = Response()
    mocked_response.text = ('Invalid response')
    monkeypatch.setattr(requests, 'get', lambda x: mocked_response)
    assert beacon(config) == [{}]


def test_beacon_nginx_exception_raised(monkeypatch):
    """Avoid returning statistics when unable to connect to nginx."""
    config = {'protocol': 'http', 'port': 80, 'host': 'localhost'}

    def mocked_get(url):
        raise requests.RequestException

    monkeypatch.setattr(requests, 'get', mocked_get)
    assert beacon(config) == [{}]
