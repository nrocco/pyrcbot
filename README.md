ircbot
======

A python module for rapidly creating ircbots.


Usage
=====

    usage: __main__.py [-h] host port channels nick password

    positional arguments:
      host        The host to connect to.
      port        The port to connect to.
      channels    Comma seperated list of channels to join.
      nick        The nickname for this bot.
      password    An optional password if required by the server you are
                  connecting to.

    optional arguments:
      -h, --help  show this help message and exit


Installation
============

Preferably in a virtual environment:

    $ git clone https://github.com/nrocco/ircbot.git 
    $ cd ircbot
    $ python setup.py install


Examples
========

Start a simple bot that outputs all IRC messages that are send and received as
debug messages to stdout.

    $ python -m ircbot irc.myserver.net 6667 #bots,#news debugbot


This will instantiate a new irc bot with `debugbot` as the nickname. The bot
will connect to `irc.myserver.net` on port `6667` and on successful connect it
will join two channels: `#bots` and `#news`.
The bot will not do anything so this is pretty useless.

