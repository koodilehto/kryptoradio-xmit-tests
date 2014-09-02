import socket
import sys
import os
import time
import select

rid_count = 5

in_sockets = []
out_sockets = []

# Delicious copypasta
def find_in_sock(sock):
    index = 0
    for m in in_sockets:
        if sock == m:
            return index
        index = index + 1
    return -1

def find_out_sock(sock):
    index = 0
    for m in out_sockets:
        if sock == m:
            return index
        index = index + 1
    return -1

# Out with the old, in with the new
for m in range(0,rid_count):
    in_sock_name = '/tmp/krin'+str(m)+".sock"
    out_sock_name = '/tmp/krout'+str(m)+".sock"
    try:
        os.unlink(in_sock_name)
    except:
        pass
    try:
        os.unlink(out_sock_name)
    except:
        pass
    in_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    out_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    in_sock.bind(in_sock_name)
    out_sock.bind(out_sock_name)
    in_sockets.append(in_sock)
    out_sockets.append(out_sock)

# Run to the hills, run for your lives
try:
    while True:
        to_read, to_write, in_error = \
            select.select(
                in_sockets,
                out_sockets,
                [], 3600)

        # Read any incoming data and pump it out
        for sock in to_read:
            index = find_in_sock(sock)
            data = sock.recvfrom(65536)
            print "Received from " + str(index) + ": " + data[0]
            if out_sockets[index] in to_write:
                try:
                    out_sockets[index].send(data[0])
                except socket.error,ex:
                    print str(ex)
except(KeyboardInterrupt, SystemExit):
    print "Keyboard interrupt."

# Cleanup
for m in range(0,rid_count):
    in_sockets[m].close()
    out_sockets[m].close()
    os.unlink('/tmp/krin'+str(m)+".sock")
    os.unlink('/tmp/krout'+str(m)+".sock")