import sys
from launchernetwork import *
import json

def host_remote():
    serve = server.main.launch_game()
    channel = RemoteChannelServer(serve)
    while True:
        channel.trigger_server()


host_remote()