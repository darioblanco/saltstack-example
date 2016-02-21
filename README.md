# Saltstack Master-Minion Vagrant set up example

## Requirements

VirtualBox >= 5.0.14
Vagrant >= 1.8.1

## What is this?

This is an example of a Saltstack master/minion configuration automatized with Vagrant, with a Virtualbox provider.

The Salt master machine is called `saltmaster`, and there is a minion example called `webserver`: an nginx serving a very simple html page.

## How to run

Start the virtual machines

> $ vagrant up salmaster webserver

They should have been automatically provisioned, if you want to reprovision the webserver, just type

> $ vagrant provision webserver

Now, just go to a browser and type the webserver IP: http://192.168.100.3/

You should see a very basic webpage provisioned by Saltmaster into the webserver minion.
