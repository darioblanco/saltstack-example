# -*- coding: utf-8 -*-
"""
Beacon to emit nginx connection status.
"""

# Import Python libs
import logging
import socket

# Import Salt libs
import salt.utils

# Import Third Party Libs
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

log = logging.getLogger(__name__)

__virtualname__ = 'nginx_connections'

VALID_PROTOCOLS = ['http', 'https']


def __virtual__():
    if salt.utils.is_windows() or HAS_REQUESTS is False:
        return False
    else:
        return __virtualname__


def validate(config):
    """Validate beacon configuration."""
    # Configuration for nginx_connections beacon should be a dict
    if not isinstance(config, dict):
        return False, ('Configuration for nginx_connections '
                       'beacon must be a dictionary.')
    else:
        # Verify configuration parameters
        if 'protocol' in config:
            if config['protocol'] not in VALID_PROTOCOLS:
                return False, ('Protocol configuration for nginx_connections '
                               'should be in {}'.format(VALID_PROTOCOLS))
        if 'port' in config:
            try:
                port = int(config['port'])
            except ValueError:
                return False, ('Port configuration for nginx_connections '
                               'is not a number.')
            else:
                if port < 1 or port > 65535:
                    return False, ('Port configuration for nginx_connection '
                                   'is not a valid port number.')
        if 'host' in config:
            try:
                socket.gethostbyname(config['host'])
            except socket.error:
                return False, ('Host configuration for nginx_connection '
                               'cannot be resolved.')
    return True, 'Valid beacon configuration'


def _get_nginx_status(**kwargs):
    """
    Send a request to the exposed nginx HttpStubStatusModule endpoint, parse
    the response and provide a statistics dictionary with connections and
    requests.
    """
    stats = {}
    url = '{protocol}://{host}:{port}{path}'.format(**kwargs)

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        log.error('Unable to connect to nginx status module in {}: {}'
                  ''.format(url, e))
    else:
        if 'server accepts handled requests' in r.text:
            lines = r.text.split('\n')
            stats['open'] = int(lines[0].split(': ')[1])
            stats['accepted'], stats['handled'], stats['requests'] = (
                int(num) for num in lines[2].split())
            stats['reading'], stats['writing'], stats['waiting'] = (
                int(num)
                for i, num in enumerate(lines[3].split())
                if i in [1, 3, 5]
            )
            log.debug('Collected nginx statistics: {}'.format(stats))
        else:
            log.error('Unable to connect to nginx status module in {}; '
                      'status code: {}, body: {}'.format(url, r.status_code,
                                                         r.text))

    return stats


def beacon(config):
    """
    Emit nginx connection status for the specified host.

    `protocol`: specifies the protocol to use (http or https).
    The default is http.

    `host`: specifies the host from where to gather the stats.
    The default is localhost.

    `port`: specifies the port from where to gather the stats.
    The default is 80.

    `path`: specifies the path where the nginx HttpStubStatusModule is running.

    .. code-block:: yaml

        beacons:
          nginx_connections:
            protocol: http
            host: localhost
            port: 8080
            path: /
    """
    log.trace('nginx_connections beacon starting')

    # Default config if not present
    if 'protocol' not in config:
        config['protocol'] = 'http'
    if 'host' not in config:
        config['host'] = 'localhost'
    if 'port' not in config:
        config['port'] = 80
    if 'path' not in config:
        config['path'] = ''

    ret = []
    stats = _get_nginx_status(**config)
    ret.append(stats)

    return ret
