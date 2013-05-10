ircbot
======

A python module for rapidly creating ircbots.


usage
-----

    usage: python -m ircbot [-h] host port channels nick password

    positional arguments:
      host        The host to connect to.
      port        The port to connect to.
      channels    Comma seperated list of channels to join.
      nick        The nickname for this bot.
      password    An optional password if required by the server you are
                  connecting to.

    optional arguments:
      -h, --help  show this help message and exit


installation
------------

Preferably in a virtual environment:

    $ git clone https://github.com/nrocco/ircbot.git
    $ cd ircbot
    $ python setup.py install


examples
--------

Here are some examples of how to use the ircbot module.


### Debug irc commands to stdout

Start a simple bot that outputs all IRC messages that are send and received as
debug messages to stdout.

    $ python -m ircbot irc.myserver.net 6667 #bots,#news debugbot


This will instantiate a new irc bot with the nickname `debugbot`. The bot will
connect to `irc.myserver.net` on port `6667` and on successful connect it will
join two channels: `#bots` and `#news`.  The bot will not do anything so this
is pretty useless.


### Make your bot do something

To add functionality to your bot you should create IrcEventHandler classes
instead of subclassing the IrcBot class. You can assign multiple handler
classes to an IrcBot instance by passing a list to the `handlers` named
argument.


### A bot that joins on invite

The following example is very simple and makes the bot auto join
channels when invited.

    from ircbot.handlers import IrcEventHandler

    class AutoJointIrcEventHandler(IrcEventHandler):

        def on_invite(self, user, channel, *args, **kwargs):
            self.client.join(channel.lstrip(':'))



    bot = IrcBot(nickname='joinbot',
                 handlers=[AutoJointIrcEventHandler()],
                 fullname='I am a bot',
                 channels=['#bots'])
    bot.connect('irc.server.com', 6667)
    bot.listen()

The irc bot above will respond to the `INVITE` irc command and will join the
channel it was invited to.
