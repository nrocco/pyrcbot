class IrcEventHandler(object):
    '''
    The base class for all other IrcEventHandler subclasses.  Every
    instance of an IrcEventHandler class will automatically be assigned
    an instance of the IrcBot class.

    You can use the instance of the IrcBot class using
    IrcEventHandler.client
    '''

    client = None


class DebugIrcEventHandler(IrcEventHandler):
    '''
    '''

    def __getattr__(self, name):
        '''
        Whenever a function is called that starts with 'on_' return the
        fallback_handler function
        '''
        if name.startswith('on_'):
            return self.fallback_handler

    def fallback_handler(self, *args, **kwargs):
        '''
        Whenver an irc event occured this Handler function will log the
        irc command and arguments passed to it.
        '''
        logger.debug('Command {} was called with args: {}'.format(
            kwargs['message'].command, args))


class CommandIrcEventHandler(IrcEventHandler):
    '''
    A base class that makes implementing a bot to which users can send
    commands (e.g. using !botname <action>). This classes listens to
    the PRIVMSG irc event and checks if the 1st argument equals the
    command_prefix.

    If this is the case it will call the on_command function on self
    passing the action and all the arguments for this action to it.

    Subclasses of the CommandIrcEventHandler class should only have to
    implement the on_command function to add functionality to this bot
    '''
    command_prefix = None

    def __init__(self, command_prefix=None, *args, **kwargs):
        '''
        If the command_prefix argument is passed to this constructor
        method it will be set on the class.  You do not have to pass the
        command_prefix argument. Alternatively you can define the
        command_prefix variable statically in your subclass.

        Will raise a ValueError if no command_prefix variable is
        defined.
        '''

        if command_prefix:
            self.command_prefix = command_prefix

        if not self.command_prefix:
            raise ValueError('CommandIrcEventHandler must have '
                             'a command_prefix')

        super(CommandIrcEventHandler, self).__init__(*args, **kwargs)

    def on_privmsg(self, origin, command='', action=None, *args, **kwargs):
        '''
        Handle the PRIVMSG irc event. Acts as a proxy method between the
        PRIVMSG irc event and the CommandIrcEventHandler.on_command. If
        the first argument equals CommandIrcEventHandler.command_prefix
        it will call the on_command method. Otherwise the PRIVMSG will
        be silently ignored.
        '''

        command = command.lstrip(':')

        if action:
            action = action.lower()

        if self.command_prefix == command:
            self.on_command(origin, command, action, *args, **kwargs)

    def on_command(self, origin, command, action=None, *args, **kwargs):
        '''
        Subclasses of CommandIrcEventHandler should implement this
        method to make the ircbot actually handle and respond to command
        actions.
        '''
        pass

