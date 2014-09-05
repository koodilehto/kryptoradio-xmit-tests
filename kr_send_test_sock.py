import socket
import sys
import os

# For writing to kryptoradio server, we need to open up an Unix domain socket
# with Datagram type. Here we connect to kryptoradio input node 0.
# On output side, all data transmitted via this node will automatically
# be received on krout0 node. Note that since the transmitter software doesn't
# need to receive anything from the kryptoradio server, we don't need to bind the socket,
# just connect and send will do.
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.connect('/tmp/krin0.sock')

# Send some simple test data. Maximum payload size is currently 64k
# The test server does not currently enforce this, however.
sock.send('This is a test!')

# Clean up after
sock.close()
