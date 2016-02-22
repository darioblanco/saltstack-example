# Saltstack Example

Trivial Master-Minion Vagrant set up example

## Requirements

Developed with:

- VirtualBox 5.0.14

- Vagrant 1.8.1

Prior versions might work, but are untested.

## What is this?

This is a very simple example of a Saltstack master/minion configuration automatized with Vagrant, with a Virtualbox provider.

The Salt master machine is called `saltmaster`, and there is a minion example called `webserver`: an nginx serving a very simple html page.

### Nginx monitoring

In addition, the nginx state uses HttpStubStatusModule for monitoring, in http://192.168.100.3:8080. Requests are restricted to vagrant's subnet (your host should have access to this subnet already). You can browse open, accepted and handled connections, and handled requests. This information will be employed by the custom SaltStack beacon.

## How to run

Start the virtual machines

> $ vagrant up saltmaster webserver

They should have been automatically provisioned, if you want to reprovision the webserver, just type

> $ vagrant provision webserver

Now, just go to a browser and type the webserver IP: http://192.168.100.3/

You should see a very basic webpage provisioned by Saltmaster into the webserver minion.

## Custom nginx_connections beacon

The minion config declares a custom `nginx_connections` beacon (developed under `roots/salt/_beacons/nginx_connections.py`), which sends nginx connection stats (see [ngx_http_stub_status_module](http://nginx.org/en/docs/http/ngx_http_stub_status_module.html)) every 10 seconds. This beacon just parses the output given by http://192.168.100.3:8080.

It is possible to see those events in `saltmaster` running in debug mode:

> $ sudo su

> $ service salt-master stop

> $ salt-master -l debug

The `webserver` minion will send them periodically:

> [DEBUG   ] Sending event - data = {'_stamp': '2016-02-22T11:40:52.006223', 'tag': 'salt/beacon/webserver.dev.darioblanco.com/nginx_connections/', 'data': {'accepted': 214, 'handled': 214, 'writing': 1, 'waiting': 0, 'requests': 217, 'reading': 0, 'open': 1, 'id': 'webserver.dev.darioblanco.com'}}
