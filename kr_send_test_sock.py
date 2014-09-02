import socket
import sys
import os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.connect('/tmp/krin0.sock')
sock.send('This is a test!')
sock.close()