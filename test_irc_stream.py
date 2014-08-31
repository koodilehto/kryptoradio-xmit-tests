# Requires twisted, pyserial, unicodecsv
# Don't ask me why ...

import serial
import os,sys
import argparse
import unicodecsv
from cStringIO import StringIO
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

parser = argparse.ArgumentParser(description='Kryptoradio Test #1.')
parser.add_argument('device', type=str, nargs=1, help='Serial device')
parser.add_argument('channel', type=str, nargs=1, help='IRC channel')
parser.add_argument('address', type=str, nargs=1, help='IRC server address')
parser.add_argument('port', type=int, nargs=1, help='IRC server port')
parser.add_argument('nick', type=str, nargs=1, help='Bot nickname')
args = parser.parse_args()

# Helper variables
device = args.device[0]
nick = args.nick[0]
channel = args.channel[0]
port = args.port[0]
address = args.address[0]
print("Using serial port device '"+device+"'.")
print("Connecting as '"+nick+"' to "+channel+" @ "+address+":"+str(port)+".")

# Try to connect
try:
    ser = serial.Serial(device, 9600, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)
except serial.serialutil.SerialException, ex:
    print(str(ex))
    exit()

# Bot itself
class KryptoBot(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "Connected to", self.factory.host, ':', self.factory.port

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as", self.factory.nickname

    def joined(self, channel):
        print "Joined channel", channel

    def privmsg(self, user, channel, msg):
        short_name = user.split('!', 1)[0]
        self.channel = channel
        f = StringIO()
        w = unicodecsv.writer(f, encoding='utf-8')
        w.writerow((short_name, msg))
        f.seek(0)
        self.factory.ser.write(f.getvalue())
        f.close()

# Factory for bots
class KryptoBotFactory(protocol.ClientFactory):
    def __init__(self, channel, nickname, host, port, ser):
        self.channel = channel
        self.nickname = nickname
        self.host = host
        self.port = port
        self.ser = ser

    def buildProtocol(self, addr):
        bot = KryptoBot()
        bot.factory = self
        return bot

    def clientConnectionLost(self, connector, reason):
        print "Connection lost: ", reason
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed: ", reason
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: ", reason

# Main
if __name__ == '__main__':
    try:
        botfactory = KryptoBotFactory(channel, nick, address, port, ser)
    except Exception as ex:
        print(str(ex))
        exit()

    reactor.connectTCP(address, port, botfactory)
    reactor.run()