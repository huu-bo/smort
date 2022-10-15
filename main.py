import json

import pygame
import random
import os
pygame.init()

size = (800, 800)

state = 'main'  # main, practice, practice_settings, editor

filenames = os.listdir('quizzes')
quiz = []
shown = []
quiz_queue = []

timer = 0
last_correct = False


def practice(f):
    global quiz, quiz_queue, state, timer, shown
    with open('quizzes/' + f, 'r') as file:
        quiz = json.load(file)
    quiz_queue = []
    shown = [False for a in quiz]

    state = 'practice'
    timer = 0


def new_learn():
    global quiz, quiz_queue, shown
    learned = True
    times = 0
    while learned and times < 100:
        i = random.randint(0, len(quiz) - 1)
        if not shown[i]:
            quiz_queue.append(quiz[i])
            shown[i] = True
            learned = False
        times += 1
    if learned:
        i = random.randint(0, len(quiz) - 1)
        quiz_queue.append(quiz[i])


pre_mouse_press = (False, False, False)
font = pygame.font.SysFont('ubuntu', size[1] // 30)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
run = True
while run:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and timer == -1 and state == 'practice':
                timer = 1

    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed(3)
    mouse_click = [mouse_press[i] and not pre_mouse_press[i] for i in range(3)]

    if state == 'main':
        y = 0
        height = size[1] // 20

        for filename in filenames:
            c = (0, 0, 0)
            if y <= mouse_pos[1] <= y + height:
                c = (50, 50, 50)
                if mouse_click[0]:
                    c = (100, 100, 100)
                    practice(filename)
            pygame.draw.rect(screen, c, (0, y, size[0], height))

            pygame.draw.rect(screen, (255, 255, 255), (0, y, size[0], height), 1)
            screen.blit(font.render(filename.split('.')[0], True, (255, 255, 255)), (0, y))

            y += height
    elif state == 'practice':
        if not quiz_queue:
            new_learn()

        screen.blit(font.render(quiz_queue[0][0], True, (255, 255, 255)), (100, 100))

        if timer == 1:
            if len(quiz_queue) > 2 - last_correct:
                if not last_correct:
                    quiz_queue.insert(2, quiz_queue[0])
                quiz_queue.pop(0)
            else:
                new_learn()
                if not last_correct:
                    quiz_queue.insert(2, quiz_queue[0])
                quiz_queue.pop(0)
            print([q[0] for q in quiz_queue])

        if timer != -1:
            y = 300
            height = size[1] // 20

            for option in quiz_queue[0][2]:
                c = (0, 0, 0)
                if timer == 0:
                    if y <= mouse_pos[1] <= y + height:
                        c = (50, 50, 50)
                        if mouse_click[0]:
                            c = (100, 100, 100)

                            if option == quiz_queue[0][1]:
                                timer = 10
                                last_correct = True
                            else:
                                timer = -1
                                last_correct = False

                pygame.draw.rect(screen, c, (0, y, size[0], height))

                pygame.draw.rect(screen, (255, 255, 255), (0, y, size[0], height), 1)
                screen.blit(font.render(option, True, (255, 255, 255)), (0, y))

                y += height + 5

        if timer > 0:
            timer -= 1

    pygame.display.update()

pygame.quit()
