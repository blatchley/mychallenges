import sys
from launchernetwork import *
import json
# Basic argument parsing and help text
def get_launch_args(args):
    if len(args) < 2:
        print("no arguments supplied, defaulting to local mode")
        return ("local", 0, 0)
    
    # if argument supplied
    mode = args[1]
    if not mode in ["remote", "r", "local", "l", "help"]:
        print("please use a valid cli command!")
        print("Run as `python launcher.py help` for more information, or read the readme")
        exit()

    if mode == "help":
        print("To test against a server or local dockerised instance of the game, connecting using IP/address and port number, use syntax")
        print("python launcher.py remote <IP/Address> <port>")
        print("or")
        print("python launcher.py r <IP/Address> <port>")
        print("\n")
        print("To test locally against the server code in this folder, simulating network communication, use parameter")
        print("python launcher.py local")
        print("or")
        print("python launcher.py l")
        print("\n")
        print("for help dialogue, launch with argument")
        print("pythong launcher.py help")
        exit()

    if mode == "l" or mode == "local":
        return ("local", 0, 0)

    if mode == "r" or mode == "remote":
        if len(args) < 4:
            print("Too few arguments, either port or ip is missing.")
            print("run with `help` argument for more information")
        try:
            ip = args[2]
            port = int(args[3])
        except Exception as e:
            print(e)
            print("failed to parse ip/port.")
            exit()
        return ("remote", ip, port)
    

from client import *
import server
def run_local():
    # print("starting local game client")
    serve = server.main.launch_game()
    channel = LocalChannel(serve)
    main.launch_game(channel)

# Run this in a docker container to host a remote server
def host_remote():
    serve = server.main.launch_game()
    channel = RemoteChannelServer(serve)
    while True:
        channel.trigger_server()

# Connect to a remote server running in a docker container, or on haaukins
def run_remote(ip,port):
    channel = RemoteChannelClient(ip, port)
    main.launch_game(channel)

# import server
    # print("starting remote game ")
    # server.main.launch_game()
    





if __name__ == "__main__":
    args = get_launch_args(sys.argv)
    if args[0] == "remote":
        run_remote(args[1],args[2])
    elif args[0] == "local":
        run_local()



# Temporary handling for stub testing. (mirror input)

# from client import *