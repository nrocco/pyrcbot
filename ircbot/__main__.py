import sys
import argparse
import logging

from ircbot.bots import IrcBot

if '__main__' == __name__:

    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)-15s %(message)s')

    parser = argparse.ArgumentParser(
        prog='python -m ircbot',
        description='Run a -- pretty useless -- ircbot')
    parser.add_argument("host", help="The host to connect to.")
    parser.add_argument("port", help="The port to connect to.", type=int)
    parser.add_argument("channels", help="Comma seperated list of "
                        "channels to join.")
    parser.add_argument("nick", help="The nickname for this bot.")
    parser.add_argument("password", help="An optional password if required "
                        "by the server you are connecting to.")
    args = parser.parse_args()

    bot = IrcBot(nickname=args.nick, 
                 password=args.password,
                 debug=True,
                 fullname='I am a bot',
                 channels=args.channels.split(','))
    bot.connect(args.host, args.port)
    retval = bot.listen()

    sys.exit(retval)

