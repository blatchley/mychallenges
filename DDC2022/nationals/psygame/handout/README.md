# Psygame: Psyducks big adventure!!!

The inevitable conclusion of realising that adding an s to pygame sounds psyduck related!

# Quickstart
Welcome our Psyduck inspired game! There are three flags in this game, each behind a different challenge. To find a flag, simply move psyduck onto the flag icon and the flag should appear in the textbox.

The game runs in a client-server setting, where the flags are on the server, and the server maintins a paralell copy of the game state. When the server things you're standing on the flag, it will send it to you. (So simply removing walls in the client which are there on the server and walking through them will just desync you from the server!)

Every input you give gets sent to the server, which then runs one game tick and replies with some data which the client may use to calculate how to handle the game tick in the same way the server did, or to display some text/information on screen.

We have packaged the game such that you can play both play against a local server in pure python, or connect to a remote server via pwntools. The folder `client` contains the game client, which renders the gui. the folder `server` contains a copy of the game server which is running on remote, (with the flags replaced with placeholders.)

To run game, run the launcher.py as follows.

To play locally against the /server folder: `python launcher.py local` 
To play against a remote server using a {PORT}/{IP}: `python launcher.py remote {PORT} {IP}`

If you run `python launcher.py` with no arguments, then it will default to local.

The controls are `wasd` or arrow keys to move around. `h` to stand still, and `esc` to exit the game.

Note: this code has been written by not one but two PhD students! As such, you can expect only the highest quality of code, comments everywhere, zero bugs and all standard design principles to have been perfectly adherred to!

Have fun! :D


# Challenges:
There are 3 challenges in this game.

To the west is the MAZE OF INVISIBLE WALLS! Make your way through the maze to claim the flag, but try not to bonk your head!

To the east is the BRIDGE OF CONFUSION! Walk down the narrow path avoiding the lava, and hope psyduck doesn't get too confused along the way!

To the north are the GATES WITHOUT KEYS! The flag is stuck behind some gates, and the keys are lost in the forest! Unfortunately the trees seem to have grown a bit taller than we originally intended, and some of the keys might have gotten lost. But we have faith that a master hacker like you can make it through!

Finally, if you're feeling especially swag, check out a (super secret) area to the south!

# Simulated remote
The version of the server running on the remote is identical to the local one, with the only difference being that the data is now sent via pwntools instead of directly handed off to the other process. Our goal was for the gameplay to be agnostic to this so you can modify your client while testing against a local server, and then as long as you haven't modified any of the game logic in the local server, the exact same client can be launched against the remote server with no difference.

For those who are interested, we have included a copy of how the server container is packaged and run in the `simulated-remote` folder. (Again with flags removed.) This shouldn't be needed to complete the challenge, but is there for those who are curious/having weird issues.
