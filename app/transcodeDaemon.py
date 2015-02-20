#!/usr/bin/env python
import os
from subprocess import call, check_output
from threading import Thread
import time
import zmq
import sys

port = "5555"


class threadConv(Thread):
    def __init__(self, dirtosearch):
        Thread.__init__(self)
        self.dirtosearch = dirtosearch

    def run(self):
        batchConv(self.dirtosearch)


def server(dirtosearch):
    tread1 = threadConv(dirtosearch)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:' + port)
    try:
        while True:
            msg = socket.recv()
            if msg == 'startconversion':
                if tread1.is_alive():
                    socket.send("Already running")
                else:
                    tread1 = threadConv(dirtosearch)
                    tread1.start()
                    socket.send("Started")

            elif msg == 'status':
                if tread1.is_alive():
                    socket.send("Already running")
                else:
                    socket.send("Not running")
            else:
                socket.send("Invalid request")
    except:
        raise
    finally:
        socket.close()


def batchConv(dirtosearch):
    mkvFiles = filesthatendswith(".mkv", dirtosearch)
    mp4Files = filesthatendswith(".mp4", dirtosearch)
    mp4Filesname = []
    print "Converting ..."
    for mp4File in mp4Files:
        mp4Filesname.append(os.path.splitext(os.path.split(mp4File)[1])[0])

    for mkvFile in mkvFiles:
        (path, filename) = os.path.split(mkvFile)
        (filename, ext) = os.path.splitext(filename)
        if not filename in mp4Filesname:
            print filename
            # print path
            convoutput = check_output(
                ["avconv", "-i", os.path.join(dirtosearch, path, filename + ".mkv"), "-c:v", "copy", "-c:a", "aac",
                 "-strict", "experimental", "-b:a", "192K", os.path.join(dirtosearch, path, filename + ".mp4")])
    print "Done"


def filesthatendswith(ext, dir):
    Files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(ext):
                Files.append(os.path.join(root, file))
    return Files


def client(msg):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 500)
    socket.connect('tcp://localhost:' + port)
    socket.send(msg)
    if socket.poll(timeout=200):
        msg = socket.recv()
    else:
        msg = "unreachable"
    print msg
    return msg


if __name__ == '__main__':
    if sys.argv[1] == "client":
        if len(sys.argv) != 3:
            print "missing command"
            sys.exit()

        print "client"
        client(sys.argv[2])
    elif sys.argv[1] == "server":
        if len(sys.argv) != 3:
            print "missing command"
            sys.exit()
        print "server"
        server(sys.argv[2])
    else:
        print "Missing argument, client [cmd] or server [folder]"
