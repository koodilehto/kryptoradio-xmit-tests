import socket
import sys
import os

try:
    os.unlink("/tmp/krclient.sock")
except:
    pass
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind('/tmp/krclient.sock')
sock.connect('/tmp/krout0.sock')
data = sock.recv(65536)
print data[0]
sock.close()