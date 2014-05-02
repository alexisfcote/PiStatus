#!/usr/bin/env python
import os
from subprocess import call, check_output
from threading import Thread
import time
import zmq
import sys

class threadConv (Thread):
    def run(self):
        batchConv()

def server():
    tread1 = threadConv()
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5555')
    try:
        while True:
            msg = socket.recv()
            if msg == 'startconversion':
                if tread1.is_alive():
                    socket.send("Already running")
                else:
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


def batchConv():
    dirtosearch = "/mnt/USBdrive/Films/transmission/test"
    mkvFiles = filesthatendswith(".mkv",dirtosearch)
    mp4Files = filesthatendswith(".mp4",dirtosearch)
    mp4Filesname = []
    for mp4File in mp4Files:
        mp4Filesname.append(os.path.splitext(mp4File)[0])

    for mkvFile in mkvFiles:
        (path,filename)=os.path.split(mkvFile)
        (filename,ext)=os.path.splitext(filename)
        if not filename in mp4Filesname:
            print filename
            convoutput = check_output(["avconv", "-i", os.path.join(dirtosearch,path,filename+".mkv"), "-c:v", "copy", "-c:a" ,"copy", os.path.join(dirtosearch,path,filename+".mp4")])


def filesthatendswith(ext,dir):
    Files = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            if file.endswith(ext):
                Files.append(file)
    return Files

def client(msg):
    context = zmq.Context()
    socket =  context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 500)
    socket.connect('tcp://localhost:5555')
    socket.send(msg)
    if socket.poll(timeout=200):
        msg = socket.recv()
    else:
        msg = "unreachable"
    print msg
    return msg



if  __name__ == '__main__':
    if sys.argv[1] == "client":
        if len(sys.argv) != 3:
            print "missing command"
            sys.exit()

        print "client"
        client(sys.argv[2])
    elif sys.argv[1] == "server":
        print "server"
        server()
    else:
        print "Missing argument, client [cmd] or server"
