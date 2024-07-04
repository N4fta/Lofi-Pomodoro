import pygame as pg
from time import sleep

# These functions will stop the program until they are finished

def fadeout(screen: pg.Surface, newScene: pg.Surface):
    for i in range(255):
        newScene.set_alpha(i)
        screen.blit(newScene, (0, 0))
        pg.display.update()
        sleep(0.05)