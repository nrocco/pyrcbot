import socket
import signal
import sys
import time
import logging

from ircbot.messages import IrcMessage
from ircbot.handlers import IrcEventHandler



SOCKET_TIMEOUT = 300
socket.setdefaulttimeout(SOCKET_TIMEOUT)

logger = logging.getLogger(__name__)

class IrcBot(object):

    irc = None

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.get('debug', True)

        self.nickname = kwargs.get('nickname', None)
        self.password = kwargs.get('password', None)
        self.fullname = kwargs.get('fullname', None)
        self.channels = kwargs.get('channels', [])
        self.handlers = kwargs.get('handlers', [IrcEventHandler()])

        for handler in self.handlers:
            handler.client = self

    def connect(self, host=None, port=None):
        self.host = host or self.host
        self.port = port or self.port
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((self.host, self.port))

        self.authorize()
        self.current_channels = []

    def disconnect(self, message=None):
        self.send('QUIT', ':%s' % message)
        self.irc.close()

    def authorize(self):
        if self.password:
            self.send('PASS', self.password)
        self.send('NICK', self.nickname)
        if None == self.fullname:
            self.fullname = self.nickname
        self.send('USER',
                  self.nickname,
                  self.nickname,
                  'baltazar',
                  ':%s' % self.fullname)
        return

    def join(self, channel):
        if isinstance(channel, list):
            channel = ','.join(channel)
        self.send('JOIN', channel)

    def leave(self, channel):
        self.send('LEAVE', channel)

    def listen(self):
        buffer = ''
        try:
            while True:
                try:
                    buffer = buffer + self.irc.recv(2048)
                    lines = buffer.split("\n")
                    buffer = lines.pop()
                except socket.error as (errno, msg):
                    if errno != 4:
                        raise

                for line in lines:
                    msg = IrcMessage(line)
                    if msg.message_length() > 0:
                        self.handle_msg_recv(msg)
                    else:
                        logger.warn('no data received')
                        return 1

        except KeyboardInterrupt:
            self.disconnect('Bye Bye!')
            return 1

        return 0

    def handle_msg_recv(self, message):
        if self.debug:
            logger.info('>>> ' + str(message))

        if 'ping' == message.command:
            self.send('PONG', message.args[0])
        elif 'join' == message.command:
            self.current_channels.append(message.args[0])
        elif 'kick' == message.command:
            self.current_channels.remove(message.args[0])
        elif 'leave' == message.command:
            self.current_channels.remove(message.args[0])
        elif 'error' == message.command:
            raise KeyboardInterrupt()
        elif '004' == message.command:
            self.join(self.channels)

        for callback_method in self.get_handlers_for(message.command):
            callback_method(*message.args, message=message)

    def get_handlers_for(self, command):
        if not self.handlers:
            return []

        method_name = 'on_{}'.format(command)
        callbacks = []

        for handler in self.handlers:
            try:
                method = getattr(handler, method_name)
            except AttributeError:
                pass
            else:
                if callable(method):
                    callbacks.append(method)

        return callbacks

    def send(self, *message):
        msg = ' '.join(message)
        if self.debug:
            logger.info('<<< ' + msg)
        self.irc.send('%s\n\r' % msg)

