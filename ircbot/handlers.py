class IrcEventHandler(object):

    client = None


class DebugIrcEventHandler(IrcEventHandler):

    def __getattr__(self, name):
        if name.startswith('on_'):
            return self.fallback_handler

    def fallback_handler(self, *args, **kwargs):
        logger.debug('Command {} was called with args: {}'.format(
            kwargs['message'].command, args))


class CommandIrcEventHandler(IrcEventHandler):
    command_prefix = None

    def __init__(self, command_prefix=None, *args, **kwargs):
        if command_prefix:
            self.command_prefix = command_prefix

        if not self.command_prefix:
            raise ValueError('CommandIrcEventHandler must have '
                             'a command_prefix')

        super(CommandIrcEventHandler, self).__init__(*args, **kwargs)

    def on_privmsg(self, origin, command='', action=None, *args, **kwargs):
        command = command.lstrip(':')

        if action:
            action = action.lower()

        if self.command_prefix == command:
            self.on_command(origin, command, action, *args, **kwargs)

    def on_command(self, origin, command, action=None, *args, **kwargs):
        pass

