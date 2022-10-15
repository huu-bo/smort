import gui
import ui

import pygame
pygame.init()

size = (800, 800)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

g = gui.gui(screen)
ui.start(g)

while not pygame.event.get(pygame.QUIT):
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed(3)

    g.render(mouse_pos, mouse_press)

    pygame.display.update()

pygame.quit()
