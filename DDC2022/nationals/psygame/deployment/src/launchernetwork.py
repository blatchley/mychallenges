import json
import pygame
import server
# import client

####################################################### 
# This is a super class for helping abstract away the difference
# between running locally (where you can edit server code to test)
#  vs running against remote (where the flags are) 
# 
# You shouldn't need to mess with any of these directly :shrug:
#######################################################
class PsygameChannel:
    def client_send(self, message : str) -> str:
        """Load in the file for extracting text."""
        pass

    def trigger_server(self, message : str) -> str:
        pass


####################################################### 
# Classes for client interacting with remove server over nc 
# These are classes used when talking to the challenge server.
# You shouldn't need to mess with any of these directly :shrug:
#######################################################
class RemoteChannelClient(PsygameChannel):
    def __init__(self, ip, port):
        from pwn import remote
        self.game = remote(ip, port, level="debug")
        self.game.recvuntil(b'Hello from the pygame community. https://www.pygame.org/contribute.html\n')

    # takes a keyboard press from the client, and sends it to the server.
    def client_send(self, user_input : str) -> dict:
        send_values = {"move":user_input}
        self.game.sendline(json.dumps(send_values).encode())
        self.game.recvuntil(b'movedata is\n')
        returned_values = json.loads(self.game.readline().strip())
        return returned_values


class RemoteChannelServer(PsygameChannel):
    def __init__(self, server_game : server.Game):
            self.server_game = server_game

    def trigger_server(self) -> str:
        command = input().strip()
        move = int(json.loads(command)['move'])
        result = self.server_game.receive_input(move)
        print(result)
        print("movedata is")
        print(json.dumps(result))

