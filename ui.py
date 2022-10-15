import gui
import pygame
import json
import os
import random


class start:
    def __init__(self, g: gui.gui):
        self.state = 'main'
        self.g = g

        self.font = self.g.font
        self.elements = []

        self.quiz = []
        self.quiz_queue = []
        self.quiz_i = 0

        self.main_mode()

    def practice_mode(self, name):
        if name + '.json' not in os.listdir('quizzes'):
            print('no')
            return
        else:
            with open('quizzes/' + name + '.json', 'r') as file:
                self.quiz = json.load(file)
        self.state = 'practice'
        self.g_clear()

        self.g_add(gui.element((0, 20, 0, 20), 'X', function=self.main_mode))

        random.shuffle(self.quiz)

        self.g_add(gui.element((0, 1, 2, 10), self.quiz[self.quiz_i][0]))
        if len(self.quiz[self.quiz_i]) == 3:
            for i in range(len(self.quiz[self.quiz_i][2])):
                self.g_add(gui.element((0, 1, i + 4, 10), self.quiz[self.quiz_i][2][i],
                                       function=self.guess,
                                       keybind=str(i + 1)))

    def main_mode(self):
        self.state = 'main'
        self.g_clear()

        self.g_add(gui.element((0, 1, 0, 1), '',
                               render=scroll_list([filename.split('.')[0] for filename in os.listdir('quizzes')],
                                                  self.font, self.practice_mode).render))

    def guess(self):
        self.quiz_i += 1

        self.g_clear()
        self.g_add(gui.element((0, 20, 0, 20), 'X', function=self.main_mode))
        self.g_add(gui.element((0, 1, 2, 10), self.quiz[self.quiz_i][0]))
        if len(self.quiz[self.quiz_i]) == 3:
            for i in range(len(self.quiz[self.quiz_i][2])):
                self.g_add(gui.element((0, 1, i + 4, 10), self.quiz[self.quiz_i][2][i],
                                       function=self.guess,
                                       keybind=str(i + 1)))

    def g_add(self, e):
        self.elements.append(e)
        self.g.add(e)

    def g_clear(self):
        for e in self.elements:
            self.g.remove(e)


class scroll_list:
    def __init__(self, items, font: pygame.font.Font, e):
        self.items = items
        self.font = font
        self.e = e  # exit

    def render(self, g: gui.gui, rect, mouse_pos, mouse_press, mouse_click):
        y = rect[0]
        height = rect[2] // 20
        for item in self.items:
            c = (0, 0, 0)
            if rect[0] <= mouse_pos[0] <= rect[0] + rect[2]:
                if y <= mouse_pos[1] <= y + height:
                    if mouse_click[0]:
                        c = (100, 100, 100)
                        self.e(item)
                    else:
                        c = (50, 50, 50)

            pygame.draw.rect(g.screen, c, (rect[0], y, rect[2], height))

            g.screen.blit(self.font.render(str(item), True, (255, 255, 255)), (rect[0] + 2, y + 2))

            pygame.draw.rect(g.screen, (255, 255, 255), (rect[0], y, rect[2], height), 1)

            y += height
