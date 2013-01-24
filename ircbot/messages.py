class IrcMessage(object):
    _line = ''
    _data = []

    def __init__(self, line):
        self._line = line.rstrip()
        self._data = self._line.split()

        try:
            if self._data[0].startswith(':'):
                self.prefix  = self._data[0][1:]
                self.command = self._data[1].lower()
                self.args    = ' '.join(self._data[2:])
            else:
                self.prefix = None
                self.command = self._data[0].lower()
                self.args    = ' '.join(self._data[1:])

            if self.args.startswith(':'):
                self.args = self.args[1:]

            if self.args:
                self.args = self.args.split()
        except:
            self.prefix = self.command = self.args = None

        self.nick, self.mode, self.user, self.host = self.parse_prefix(self.prefix)

    def parse_prefix(self, prefix):
        if not prefix:
            return (None, None, None, None)
        try:
            nick, rest = prefix.split('!')
        except ValueError:
            return (prefix, None, None, None)
        try:
            mode, rest = rest.split('=')
        except ValueError:
            mode, rest = None, rest
        try:
            user, host = rest.split('@')
        except ValueError:
            return (prefix, mode, rest, None)
        return (nick, mode, user, host)

    def __str__(self):
        return self._line

    def __getitem__(self, key):
        return self._data[key]

    def message_length(self):
        return len(self._line)
