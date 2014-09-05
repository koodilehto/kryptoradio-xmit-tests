import socket
import sys
import os
import time
import select

# How many RID's we allocate. 3 for now.
rid_count = 3

in_sockets = []
out_sockets = []
all_sockets = []
mappings = {}

def sock_is_output(sock):
    if sock in out_sockets:
        return True
    return False

def sock_is_input(sock):
    if sock in in_sockets:
        return True
    return False

def try_unlink(filename):
    try:
        os.unlink(filename)
    except:
        pass

# Out with the old, in with the new
for m in range(0,rid_count):
    # Form socket names and try to clean up any old sockets
    in_sock_name = '/tmp/krin'+str(m)+".sock"
    out_sock_name = '/tmp/krout'+str(m)+".sock"
    try_unlink(in_sock_name)
    try_unlink(out_sock_name)

    # Create the new sockets and bind them here.
    in_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    out_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    in_sock.bind(in_sock_name)
    out_sock.bind(out_sock_name)

    # Add the sockets to some data structures.
    in_sockets.append(in_sock)
    out_sockets.append(out_sock)
    mappings[in_sock] = out_sock
    mappings[out_sock] = in_sock
    all_sockets.append(in_sock)
    all_sockets.append(out_sock)

# Run to the hills, run for your lives
try:
    while True:
        to_read, to_write, in_error = \
            select.select(
                all_sockets,
                all_sockets,
                [], 3600)

        for in_sock in to_read:
            # Read any incoming data, and connect socket to input automatically
            # The connecting socket needs to be bound for this to work, however.
            packet = in_sock.recvfrom(65536)
            if packet[1] != None:
                print "Socket registered with string: " + packet[0]
                in_sock.connect(packet[1])

            # Dump any incoming data to output, if outgoing socket is ready
            # and incoming data is from input socket
            if sock_is_input(in_sock):
                data = packet[0]
                print "Received: " + data
                if mappings[in_sock] in to_write:
                    try:
                        mappings[in_sock].send(data)
                    except socket.error,ex:
                        print str(ex)
                time.sleep(len(data) / 960)
except(KeyboardInterrupt, SystemExit):
    print "Keyboard interrupt."

# Cleanup
for m in range(0,rid_count):
    in_sockets[m].close()
    out_sockets[m].close()
    os.unlink('/tmp/krin'+str(m)+".sock")
    os.unlink('/tmp/krout'+str(m)+".sock")
