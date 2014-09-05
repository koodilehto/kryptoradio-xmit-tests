import socket
import sys
import os

# Our own socket name
self_socket_name = '/tmp/krclient.sock'

# Socket we want to connect to
connect_sock_name = '/tmp/krout0.sock'

# Just try to clean up our old socket.
def try_unlink(filename):
    try:
        os.unlink(filename)
    except:
        pass

# Create a new socket, and bind it to our own socket file
# Binding must be done so that the server knows where to write stuff
# that belongs to us.
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(self_socket_name)

# Connect this socket to kryptoradio test program output socket.
# The output socket name must match the input socket number. Eg. krin0 -> krout0.
sock.connect(connect_sock_name)

# For the server to notice that it has a client in a socket, we have to write it something, anything.
# Just "x" will do.
sock.send('x')

# Attempt to receive data. The maximum is currently 65k.
data = sock.recv(65536)
print data

# Cleanup.
sock.close()
try_unlink(self_socket_name)
