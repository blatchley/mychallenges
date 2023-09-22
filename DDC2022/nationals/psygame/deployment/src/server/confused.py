import random
import os

def get_confused():
    # psyduck got confused, so we need some suitably random confusion!
    rseed = os.urandom(32).hex()
    random.seed(rseed)

def get_confused_move():
    return random.randint(0, 4294967294)