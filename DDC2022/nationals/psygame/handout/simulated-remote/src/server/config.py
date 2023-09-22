import pygame
from .flags import maze_flag, bridge_flag, gate_flag

WIN_WIDTH = 1024
WIN_HEIGHT = 768
TILESIZE = 32

SIGN_LAYER = 10
ITEM_LAYER = 6
PLAYER_LAYER = 5
GATE_LAYER = 4
BLOCK_LAYER = 3
LAVA_LAYER = 2
GROUND_LAYER = 1

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
DARK_BLUE = (0, 0, 168)


FPS = 10

# valid user inputs
VALID_BUTTONS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_h]


level_1 = [
    'BBBBBBBBBBBBBBB44BBBBBBBBBBBBBBB',
    'B.............SRR..............B',
    'B..........B...RR.......BBBB...B',
    'B..BBB.........RR..............B',
    'B..............RR........B.....B',
    'B..............RR...BB.........B',
    'B........BBB...RR.........BB...B',
    'B..............RR..............B',
    'B..............RR..............B',
    'B..............RR..............B',
    'B..............RR..............B',
    'B....BBBB......RR.....BBBB.....B',
    'B..............RR..............B',
    'BS.............RR.............SB',
    '2RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR3',
    '2RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR3',
    'B..........B..P................B',
    'B..........B...................B',
    'B..........BBBBBB.....B........B',
    'B..........B..........B........B',
    'B.....................B...BB...B',
    'B.....................B........B',
    'B......BBBB...........B........B',
    'B.....................B........B',
    'B.....................B........B',
    'B.....................B........B',
    'B.....................B........B',
    'B..........................B...B',
    'B.......BB.....................B',
    'B.............S................B',
    'BBBBBBBBBBBBBBB55BBBBBBBBBBBBBBB',
    ("sign",(1,13), "Level 1: The Invisible Maze!"),
    ("sign",(14,1), "Level 3: The Gates without keys!"),
    ("sign",(30,13), "Level 2: The Bridge of Confusion!"),
    ("sign",(14,29), "Swag Shop!"),
]

level_2 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..................XXYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYXXXXXXXXXXXXXXXXXXXXXXXXXXXXX..............B',
    'B..................XXYXXXXXXXXXXXXXXXXXXXXXXXXXXXXYYYYYYYYYYYYYYXXXXXXXXXXXXXXXX..............B',
    'B..................XXYYYYYYYYYYYYYXXXXXYXXXXXXXXXXYXXXXXXXXXXXXYXXXXYYYYYYYYYXXX..............B',
    'B..................XXXXXXXXXXXXXXYYYYYYYXXXXXXXXXXYXXXXXXXXXXXXYXXXXYXXXXXXXYXXX..............B',
    'B..................XXXXXXXXXXXXXXYXXXXXXXXXXXXYYYYYXXXXXXXXXXXXYXXXXYXXXXXXXYXXX..............B',
    'B..................XXXXXXXXXXXXXXYXXXXXXXXXXXXYXXXYYYYYYYXXXXXXYXXXXYXXXXXXXYXXX..............B',
    'B..................XXXXXXXXXXXXXXYXXXXXXXXXXXXYXXXXXXXXXYXXXXXXYXXXXYXXXXXXXYXXX..............B',
    'B..................XXXXXXXXXXXXXXYXXXXXXXXXXXXYXXXXXXXXXYXXXXXXYYYYYYYYYYXXXYXXX..............B',
    'B..................XXXXXXXXXXXXXXYXXXXXXXXXXXXYXXXXXXXXXYXXXXXXXXXXXXXXXYXXXYXXX........S...RR1',
    'B..................XFYYYYYYYYYYYYYXXXXXXXXXXXXYXXXXXXXXXYXXXXXXXXXXXXXXXYXXXYYYY...........PRR1',
    'B..................XXXXXXXXXXXXXXXXXXXYYYYYYYYYXXXXXXXXXYXXXXXXXXXXXXXXXYXXXXXXX..............B',
    'B..................XXXXXXXYXXXXXXXYYYYYXXXXXXXXXXXXXXXXXYXXXXXXXXXXXXXXXYXXXXXXX..............B',
    'B..................XXXXXXXYXXXXXXXYXXXXXXXXXXXXXXXXXXXXXYXXXXXXXXXXXXXXXYXXXXXXX..............B',
    'B..................XXXXXXXYXXXXXXXYXXXXXXXXYXXXXXYYYYYYYYXXXXXXXYYYYYYYYYYYYYXXX..............B',
    'B..................XXXXXXXYYYYYYYYYYYYYYYYYYXXXXXYXXXXXXXXXXXXXXYXXXXYXXXXXXYXXX..............B',
    'B..................XXXYYYYYXXXXXXXXXXXXXXXXYXXXXXYXXXXXXXXXXXXXXYXXXXYXXXXXXYXXX..............B',
    'B..................XXXXXXXXXXXXXXXXXXXXXXXXYYYYYYYYYYYYYYYYYYYYYYXXXXYXXXXXXYXXX..............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    ("sign",(88,9), "The flag is at the end of this maze. Unfortunatley the path is invisible..."),
    ("sign",(20,10), maze_flag)
]


level_3 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............................LLL..LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL...LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLB',
    'B............................L..LL...LLLLLLLLLLLLLLLLLL..LLLLLLLLLL...LLLLLLL...LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLB',
    'B.......S.........................LL..LLLLLLLL.....LLL.....LLLLLLL.....LLLLLLLLLLLLLLLL........LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL......LLLLLLLLLLLLLLLLB',
    '1RR.P...............................C.......................................................................................................F.LLLLLLLLLLLLLLLLB',
    '1RR.................................C.LLLL.......LLLLLLLLL......LLLL....LLLLLLLLLLLL...LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.....LLLLLLLLLLLLLLLLB',
    'B..............................L.LLLL...LLLLL.......LLLLLLLL..LLLLLLLLLLLLLL.....LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLB',
    'B...............................LLLLLLLLLLLLLLLLL....LLLLLLLLLL..LLLLLL..LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLB',
    'B..............................L..LLLLLLLLLLLLLLLLLLLLLLLLLLL......LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    ("sign",(8,3), "The flag is just past all the lava. Try not to get too confused!"),
    ("sign",(140,4), bridge_flag),
]

level_4 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BAAAAAAAAAAAAAAAAAAA.........W.F.W.....T....T......BB...............B',
    'BAAAAAAAAAAAAAAAAAAA..T......W...W........BB...T...BBBB.....T..T.T..B',
    'BAAAAAAAAAAAAAAAAAAA......T..WWGWW.........BT........BIT.....T.....IB',
    'BAAAAAAAAAAAAAAAAAAA.........W...W.....T...B..T.......B.............B',
    'BAAAAAAAAAAAAAAAAAAA.........WWGWW....B....T.....T..BBB....T...T..T.B',
    'BAAAAAAAAAAAAAAAAAAA.........W...W.....B.....T....T.........T.......B',
    'BAAAAAAAAAAAAAAAAAAA.........WWGWW.........B..T.......T........T....B',
    'BAAAAAAAAAAAAAAAAAAA....S...................BT..T.....B......T......B',
    'BAAAAAAAAAAAAAAAAAAA.........P...................T.BBT.....T..T.T.T.B',
    'BAAAAAAAAAAAAAAAAAAA.........RR....................BI...............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBB11BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    ("sign", (24,8), "The gate keys were lost in the forest, but then the trees grew!"),
    ("sign", (31,1), gate_flag),
    ("item", (52,10), "key"),
    ("item", (67,3), "key")
]

level_5 = [
    'BBBBBBBBBBBBBBB11BBBBBBBBBBBBBBB',
    'B.............BRRB.............B',
    'B.............BP.B.............B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B.............B..B.............B',
    'B............B....B............B',
    'B...........B......B...........B',
    'B..........B........B..........B',
    'B.........B..........B.........B',
    'B........B.....SI.....B........B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    ("sign", (15,14), "Wanna look cool?"),
    ("item", (16, 14), "cool_sunglasses")
]

# network class
class PsygameChannel:
    def client_send(self, message : str) -> str:
        pass

    def trigger_server(self, message : str) -> str:
        pass