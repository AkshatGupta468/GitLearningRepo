import random, sys, pygame, os
from pygame.locals import *
from time import sleep

FPS = 32

LOC = os.getcwd()
drives = ("C:", "D:", "E:", "F:", "G:", "H:")

print(os.getcwd())
print(LOC)

SCREENWIDTH = 490
SCREENHEIGHT = 450
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = 311
GAMESPRITES = {}
GAMESOUNDS = {}

# t = pfygame.font.Font("calibribody",32)

def welcome_scr():
    """
    shows welcome screen
    :return:
    """
    pygame.mixer.Channel(1).unpause()
    playerx = int(SCREENWIDTH / 15)
    playery = int((SCREENHEIGHT - GAMESPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAMESPRITES['tittle'].get_width()) * 0.1)
    messagey = int(0.05 * SCREENHEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE):
                return
            else:
                SCREEN.blit(GAMESPRITES['background'], (0, 0))
                SCREEN.blit(GAMESPRITES['player'], (playerx, playery))
                SCREEN.blit(GAMESPRITES['tittle'], (messagex, messagey))
                SCREEN.blit(GAMESPRITES['base'], (0, GROUNDY))
                SCREEN.blit(GAMESPRITES['press'], (0, GROUNDY - GAMESPRITES['press'].get_height()))
                if (score > 0):
                    print_score(score)

                pygame.display.update()
                FPSCLOCK.tick(FPS)


def touch(pipe, playerx, playery):
    if (pipe[0]['x'] > 46 and pipe[0]['x'] < 150):
        if ((pipe[0]['y']['up'] + GAMESPRITES['pipe'][1].get_height() > playery + 5) and (
                pipe[0]['x'] + 10 - (playerx + GAMESPRITES['player'].get_width()) < 0)):
            return True
        elif ((pipe[0]['y']['down'] < playery + GAMESPRITES['player'].get_height() - 2) and (
                pipe[0]['x'] + 10 - (playerx + GAMESPRITES['player'].get_width()) < 0)):
            return True
    return False


def print_score(pipe_no):
    if (pipe_no < 10):
        SCREEN.blit(GAMESPRITES['num'][pipe_no], ((SCREENWIDTH - GAMESPRITES['num'][pipe_no].get_width()) / 2, 50))
    elif (pipe_no >= 10):
        tens = int(pipe_no / 10)
        ones = int(pipe_no % 10)
        SCREEN.blit(GAMESPRITES['num'][tens], (int(SCREENWIDTH / 2 - GAMESPRITES['num'][tens].get_width()), 50))
        SCREEN.blit(GAMESPRITES['num'][ones], (int(SCREENWIDTH / 2), 50))


f = 3


def maingame(see):
    pygame.mixer.music.pause()
    pipe_no = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAMESPRITES['player'].get_height()) / 2)
    basex = [0, SCREENWIDTH]
    vel_y = 0
    vel_x = 8
    acc_y = 4
    acc_flap = -5
    val = see[1]
    pipe = [{'x': SCREENWIDTH, 'y': {'up': -140, 'down': 200}},
            {'x': int(SCREENWIDTH * 1.8), 'y': {'up': val, 'down': val + 340}}]
    while True:
        SCREEN.blit(GAMESPRITES['background'], (0, 0))
        SCREEN.blit(GAMESPRITES['pipe'][1], (pipe[0]['x'], pipe[0]['y']['up']))
        SCREEN.blit(GAMESPRITES['pipe'][0], (pipe[0]['x'], pipe[0]['y']['down']))
        SCREEN.blit(GAMESPRITES['pipe'][1], (pipe[1]['x'], pipe[1]['y']['up']))
        SCREEN.blit(GAMESPRITES['pipe'][0], (pipe[1]['x'], pipe[1]['y']['down']))
        # SCREEN.blit(GAMESPRITES['player'], (playerx, playery))
        SCREEN.blit(GAMESPRITES['base'], (basex[0], GROUNDY))
        SCREEN.blit(GAMESPRITES['base'], (basex[1], GROUNDY))
        SCREEN.blit(GAMESPRITES['uparrow'], ((SCREENWIDTH - GAMESPRITES['uparrow'].get_width()) / 2, GROUNDY + 30))
        global f
        SCREEN.blit(GAMESPRITES['bird'][int(f / 3)], (playerx, playery))
        if (f < 27 and f > 3):
            f += 1
        elif (f == 27):
            f = 5

        print_score(pipe_no)
        playery = playery + vel_y
        vel_y = vel_y + acc_y
        pipe[0]['x'] = pipe[0]['x'] - vel_x
        pipe[1]['x'] = pipe[1]['x'] - vel_x
        basex[0] = basex[0] - vel_x
        basex[1] = basex[1] - vel_x

        if (pipe[0]['x'] < -50):
            pipe[0]['x'] = pipe[1]['x']
            pipe[0]['y']['up'] = pipe[1]['y']['up']
            pipe[0]['y']['down'] = pipe[1]['y']['down']
            val = see[pipe_no]
            pipe_no = pipe_no + 1
            pipe[1]['x'] = pipe[0]['x'] + int(SCREENWIDTH * 0.8)
            pipe[1]['y']['up'] = val
            pipe[1]['y']['down'] = val + 350

        if (basex[0] <= -SCREENWIDTH):
            basex[0] = basex[1]
            basex[1] = SCREENWIDTH

        acc_y = 0.2
        if (vel_y > 12):
            vel_y = 12
        elif (vel_y < -8):
            vel_y = -8
        if (playery + GAMESPRITES['player'].get_height() >= GROUNDY):
            vel_y = int(-(0.6) * vel_y)
        elif (playery < 15):
            acc_y = 1
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_UP):
                vel_y = vel_y + acc_flap
                pygame.mixer.Sound.play(GAMESOUNDS['jump']).set_volume(0.3)
                f = 4
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        if (touch(pipe, playerx, playery)):
            pygame.mixer.Channel(0).pause()
            pygame.mixer.Sound.play(GAMESOUNDS['death']).set_volume(0.50)
            return pipe_no


score = 0
if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('BALL JUMP')
    GAMESPRITES['pipe'] = (pygame.image.load(r'{}'.format(LOC) + "/images/pipe.png").convert_alpha()
                           , pygame.transform.rotate(
        pygame.image.load(r'{}'.format(LOC) + "/images/pipe.png").convert_alpha(), 180)
                           )
    GAMESPRITES['background'] = pygame.image.load(r'{}'.format(LOC) + "/images/background.png").convert()
    GAMESPRITES['player'] = pygame.image.load(r'{}'.format(LOC) + "/images/player.png").convert_alpha()
    GAMESPRITES['bird'] = {}
    for i in range(1, 10):
        GAMESPRITES['bird'][i] = pygame.image.load(r'{}'.format(LOC) + "/images/bird" + str(i) + ".png").convert_alpha()
    GAMESPRITES['loading'] = pygame.image.load(r'{}'.format(LOC) + "/images/loading" + ".png").convert_alpha()
    GAMESPRITES['bar'] = pygame.image.load(r'{}'.format(LOC) + "/images/bar" + ".png").convert_alpha()
    GAMESPRITES['barbit'] = pygame.image.load(r'{}'.format(LOC) + "/images/barbit" + ".png").convert_alpha()

    GAMESPRITES['base'] = pygame.image.load(r'{}'.format(LOC) + "/images/base.png").convert_alpha()
    GAMESPRITES['tittle'] = pygame.image.load(r'{}'.format(LOC) + "/images/tittle.png").convert_alpha()
    GAMESPRITES['press'] = pygame.image.load(r'{}'.format(LOC) + "/images/press.png").convert_alpha()
    GAMESPRITES['uparrow'] = pygame.image.load(r'{}'.format(LOC) + "/images/uparrow.png").convert_alpha()
    GAMESPRITES['num'] = {}
    for i in range(10):
        GAMESPRITES['num'][i] = pygame.image.load(r'{}'.format(LOC) + "/images/num" + str(i) + ".png").convert_alpha()

    GAMESOUNDS['background'] = pygame.mixer.Sound(r"{}".format(LOC) + "/music/Kalimba.mp3")
    GAMESOUNDS['jump'] = pygame.mixer.Sound(r"{}".format(LOC) + "/music/jump.mp3")
    GAMESOUNDS['death'] = pygame.mixer.Sound(r"{}".format(LOC) + "/music/death.mp3")
    GAMESOUNDS['entry'] = pygame.mixer.Sound(r"{}".format(LOC) + "/music/entry.mp3")
    pygame.mixer.Channel(0).play(GAMESOUNDS['background'], 100)
    GAMESOUNDS['background'].set_volume(0.7)
    pygame.mixer.Channel(0).pause()

    pygame.mixer.Channel(1).play(GAMESOUNDS['entry'], 100)

    SCREEN.blit(GAMESPRITES['loading'], (SCREENWIDTH / 2 - GAMESPRITES['loading'].get_width() / 2,
                                         SCREENHEIGHT / 2 - GAMESPRITES['loading'].get_height() / 2))
    SCREEN.blit(GAMESPRITES['bar'], (SCREENWIDTH / 2 - GAMESPRITES['bar'].get_width() / 2,
                                     SCREENHEIGHT / 2 + GAMESPRITES['loading'].get_height() / 2))
    for i in range(40):
        SCREEN.blit(GAMESPRITES['barbit'],
                    (SCREENWIDTH / 2 - GAMESPRITES['bar'].get_width() / 2 + i * GAMESPRITES['barbit'].get_width(),
                     SCREENHEIGHT / 2 + GAMESPRITES['loading'].get_height() / 2))
        pygame.display.update()
        sleep(0.35)
    while True:
        welcome_scr()
        pygame.mixer.Channel(1).pause()

        see = []
        for i in range(1000):
            see.append(random.randint(-180, 0))
        score = 0
        pygame.mixer.Channel(0).unpause()
        score = maingame(see)
        sleep(3)
