#!/usr/bin/env python

import sys, os
import pickle
import time
import signal
import traceback
import webbrowser

CONFIG_PATH = '.sublime2note-server'
config = None
server_port = 5000
server_pid = -1

if os.path.isfile(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = pickle.load(f) 
        server_pid = config['server_pid']
        server_port = config['server_port']

def kill_server():
    if server_pid >= 0:
        try:
            os.kill(server_pid, signal.SIGKILL)
        except Exception, e:
            pass
        try:
            os.remove(CONFIG_PATH)
        except Exception, e:
            pass
        print "killed pid=%d" % server_pid

def inquire_server():
    if os.path.isfile(CONFIG_PATH):
        print "[STARTED] Server is running on process %d, listening on 127.0.0.1:%d" % (server_pid, server_port)
    else:
        "[STOPPED] Server is not running."

import subprocess
def run_server():
    proc = subprocess.Popen("python server.py %d" % server_port, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    server_pid = proc.pid
    with open(CONFIG_PATH, 'w') as f:
        pickle.dump({'server_pid':server_pid, 'server_port':server_port},f)
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:%d' % server_port)

import socket
def get_unused_port():
  my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  my_socket.bind(('localhost', 0))
  addr, port = my_socket.getsockname()
  my_socket.close()
  return port

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Sublime2Note Server Tool')
    parser.add_argument('command', type=str, help='Server command: [ start | stop | status | finish ]')
    args = parser.parse_args()

    if args.command == 'start':
        kill_server()
        server_port = get_unused_port()
        run_server()
        inquire_server()
    elif args.command == 'stop':
        kill_server()
    elif args.command == 'status':
        inquire_server()
    elif args.command == 'finish':
        # make sure user get the "connected" page.
        time.sleep(3)
        kill_server()
    else:
        print 'Unrecognizable command.'
        exit(-1)


