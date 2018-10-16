__author__ = 'User'

import pygame
from pygame import time
from pygame.locals import *
from Game import GameObject

from Main import init, load, update
from Graphics.Camera import Camera
from Input.Keyboard import Keyboard
from Input.Mouse import Mouse

from Resources import ResourceManager
import socket, threading
def debug():
    print "bug"

def _init(game):
    print "Initializing"
    pygame.init()

    game.screen = pygame.display.set_mode((game.width, game.height))
    pygame.display.set_caption(game.name)

    game.clock = time.Clock()
    game.frame = 0

    # Create background
    game.background = pygame.Surface(game.screen.get_size())
    game.background = game.background.convert()
    game.background.fill((250,250,250))

    game.camera = Camera()

    # Setup input
    game.keyboard = Keyboard()
    game.mouse = Mouse()

    game.resources = ResourceManager()
    '''
    # Init actor list
    game["actors"] = ActorList()
    #game["entities"] = EntityList()
    game["gui"] = GuiManager(game)

    game["socket"] = socket.socket()

    ut_server_recv = threading.Thread(target=server_update, args=(game,))
    #ut_server_recv.start()

    game["ut_socket"] = ut_server_recv
    '''
    _load_resources(game)
    init(game)
    return 1

def _load_resources(game):

    game.resources.load("defaultTexture", "Textures/default.png", ResourceManager.IMAGE)
    game.default_font = pygame.font.SysFont("monospace", 16)
    load(game)


def _loop(game):
    print "Starting game loop"
    while True:
        # Updates the game clock
        game.clock.tick(60)
        game.frame += 1
        # Handle events
        '''
        for guiActor in game["gui"].items:
            x, y = game["mouse"].X, game["mouse"].Y
            if guiActor.X < x < guiActor.X + guiActor.Width and guiActor.Y < y < guiActor.Y + guiActor.Height:
                pass
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                #game["socket"].close()
                #game["ut_socket"].kill()
                return 1
            if event.type == KEYDOWN or event.type == KEYUP:
                game.keyboard.handle(event)
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
                game.mouse.handle(event)

        for key in game.keyboard.pressed_keys:
            game.keyboard.exec_list(game.keyboard.keys[key]["events"]["click"])

        #game["entities"].update(game)


        update(game)

        game.screen.blit(game.background, (0,0))
        game.scenes[game.current_scene].draw()
        pygame.display.flip()

def main():
    game = GameObject()

    if _init(game):
        game.status = GameObject.READY
        _loop(game)

if __name__ == '__main__':
    main()
