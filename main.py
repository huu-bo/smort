#!/usr/bin/python3

import json
import enum
import pygame
import random
import os
pygame.init()

# choose by clicking,
# e for editor
# you can use 1, 2, 3, 4 buttons in the player

# big word/words is/are the question(s)
# number in top right is % correctness

# TODO: different font (circumflex broken)

size = (800, 800)
settings = {
    'mode': 'choice'  # choice, type
}
DELAY = 2  # should be more than 1
Q_DELAY = [
    4, 10, 20, 30, 40, 50, 50, 50
]  # the delay of how many questions you need to answer before a question that you answered correct is repeated

state = 'main'  # main, practice, practice_settings, editor

filenames = os.listdir('quizzes')


def load(directory):
    if not os.path.isdir(directory):
        print(directory, 'not a directory')
        return [['error', 'error', True, [], False]]

    out = []
    for filename in os.listdir(directory):
        d = os.path.isdir(directory + '/' + filename)
        if d:
            out.append([filename, directory + '/' + filename, True, load(directory + '/' + filename), False])
        else:
            out.append((filename, directory + '/' + filename, False))
    return out


qs = load('quizzes')


class QS(enum.IntEnum):
    DRAW_NAME = 0
    FILE_NAME = 1
    FOLDER = 2
    FOLDER_CONTENT = 3
    FOLDER_SELECTED = 4


quiz = []
shown = []
quiz_queue = []
quiz_schedule = []
correct_streak = {}

timer = 0
last_correct = False
typing = ''

q_selection = 0
q_ret = False

correct = [0., {}]

editing = [False, []]


def practice(f):
    global quiz, quiz_queue, state, timer, shown, Q_DELAY, correct
    with open(f, 'r', encoding='UTF-8') as file:
        quiz = json.load(file)

    if len(quiz) > Q_DELAY[-1]:
        print('quiz too long')
    correct = [0., {}]
    for q in quiz:
        if len(q) == 2:
            answers = []
            c = random.randint(0, 3)
            for i in range(4):
                if i == c and q[1] not in answers:
                    answers.append(q[1])
                else:
                    if len(quiz) < 5:  # 5 is just a guess it's probably lower
                        raise Exception('quiz should have more than 5 questions')
                    good = False
                    while not good:  # terrible code
                        p = random.randint(0, len(quiz) - 1)
                        if quiz[p][1] not in answers:
                            answers.append(quiz[p][1])
                            good = True
            q.append(answers)
        elif len(q) != 3:
            print('not enough or too much information', q)

    quiz_queue = []
    shown = [False for _ in quiz]

    state = 'practice'
    timer = 0


def editor():
    global state, editing
    state = 'editor'
    editing = [False, []]


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


def guess(option):
    global quiz_queue, timer, last_correct, settings, quiz, DELAY, correct
    if option == quiz_queue[0][1]:
        timer = DELAY
        last_correct = True
    else:
        timer = -1
        last_correct = False

        for q in quiz:
            if q != quiz_queue[0]:
                if option in q[1]:
                    quiz_queue.append(q)  # add all questions that have the answer that you gave
        good = True
        for a in option.replace(' ', '').split(','):
            if a not in quiz_queue[0][1].replace(' ', '').split(','):
                good = False
        if good:
            last_correct = True
            timer = DELAY

    if quiz_queue[0][0] not in correct[1]:
        correct[1][quiz_queue[0][0]] = False
    if not last_correct:
        if correct[1][quiz_queue[0][0]]:
            correct[1][quiz_queue[0][0]] = False
            correct[0] -= 1 / len(quiz)
    else:
        if not correct[1][quiz_queue[0][0]]:
            correct[1][quiz_queue[0][0]] = True
            correct[0] += 1 / len(quiz)

    if settings['mode'] == 'type' and not last_correct:
        out = []
        out += option


def draw_files(qs, y: int, level: int, selected: int, ret: bool):
    height = size[1] // 20

    for q in qs:
        # print(q)
        c = (0, 0, 0)
        if y <= mouse_pos[1] <= y + height or selected == y // height:
            c = (50, 50, 50)
            if mouse_click[0] or ret:
                c = (100, 100, 100)
                if not q[QS.FOLDER]:
                    practice(q[QS.FILE_NAME])
                else:
                    q[QS.FOLDER_SELECTED] = not q[QS.FOLDER_SELECTED]

        if not q[QS.FOLDER]:
            pygame.draw.rect(screen, c, (0, y, size[0], height))

            pygame.draw.rect(screen, (255, 255, 255), (level * height, y, size[0] - level * height, height), 1)
            screen.blit(font.render(''.join(q[QS.DRAW_NAME].split('.')[0]), True, (255, 255, 255)), (level * height, y))

            y += height
        else:
            pygame.draw.rect(screen, c, (0, y, size[0], height))

            pygame.draw.rect(screen, (255, 255, 255), (level * height, y, size[0] - level * height, height), 1)
            screen.blit(font.render('/ ' + ''.join(q[QS.DRAW_NAME].split('.')[0]), True, (255, 255, 255)), (level * height, y))

            y += height

            if q[QS.FOLDER_SELECTED]:
                y += draw_files(q[QS.FOLDER_CONTENT], y, level + 1, selected, ret) - y
    return y


pre_mouse_press = (False, False, False)
# font = pygame.font.SysFont('ubuntu', size[1] // 30)
font = pygame.font.Font('font/ubuntu.ttf', size[1] // 30)
big_font = pygame.font.Font('font/ubuntu.ttf', size[1] // 20)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
run = True
frame = 0
while run:
    clock.tick(60)
    screen.fill((0, 0, 0))
    q_ret = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and timer == -1 and state == 'practice':
                timer = 1
            elif state == 'practice':
                if settings['mode'] == 'choice':
                    if event.key == pygame.K_1:
                        if 0 <= len(quiz_queue[0][2]):
                            guess(quiz_queue[0][2][0])
                    if event.key == pygame.K_2:
                        if 1 <= len(quiz_queue[0][2]):
                            guess(quiz_queue[0][2][1])
                    if event.key == pygame.K_3:
                        if 2 <= len(quiz_queue[0][2]):
                            guess(quiz_queue[0][2][2])
                    if event.key == pygame.K_4:
                        if 3 <= len(quiz_queue[0][2]):
                            guess(quiz_queue[0][2][3])

                    if event.key == pygame.K_e:
                        editor()
                    if event.key == pygame.K_m:
                        settings['mode'] = 'type'
                else:
                    if event.key == pygame.K_RETURN and timer == 0:
                        guess(typing)
                        typing = ''
                    elif event.key == pygame.K_BACKSPACE:
                        typing = typing[:-1]
                    elif event.key == pygame.K_m and event.mod & pygame.KMOD_CTRL:
                        settings['mode'] = 'choice'
                    else:
                        typing += event.unicode

                if event.key == pygame.K_ESCAPE:
                    state = 'main'
            elif state == 'editor':
                if event.mod & pygame.KMOD_CTRL:
                    if event.key == pygame.K_e:
                        state = 'main'
                    if event.key == pygame.K_n:
                        editing = [1, ['', '']]
                else:
                    if not editing[1]:
                        editing[1].append('')
                        editing[1].append('')
                    if event.key == pygame.K_RETURN:
                        if editing[0] < 3:
                            editing[0] += 1
                    elif event.key == pygame.K_BACKSPACE:
                        editing[1][0] = editing[1][0][:-1]
                    else:
                        editing[1][editing[0] - 1] += event.unicode
            elif state == 'main':
                if event.key == pygame.K_DOWN:
                    q_selection += 1
                elif event.key == pygame.K_UP:
                    if q_selection > 0:
                        q_selection -= 1
                if event.key == pygame.K_RETURN:
                    q_ret = True

    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed(3)
    mouse_click = [mouse_press[i] and not pre_mouse_press[i] for i in range(3)]

    if state == 'main':
        draw_files(qs, 0, 0, q_selection, q_ret)

    elif state == 'practice':
        if not quiz_queue:
            new_learn()

        screen.blit(big_font.render(quiz_queue[0][0], True, (255, 255, 255)), (100, 100))
        screen.blit(font.render(str(round(correct[0] * 100)), True, (255, 255, 255)), (size[0] - 50, 50))

        if timer == 1:
            if len(quiz_queue) > 2 - last_correct:
                pass
            else:
                new_learn()

            if not last_correct:
                quiz_queue.insert(2, quiz_queue[0])

            found = False
            for q in quiz_schedule:
                if quiz_queue[0][0] == q[0]:
                    found = True
            if not found:
                if last_correct:
                    if quiz_queue[0][0] not in correct_streak:
                        correct_streak[quiz_queue[0][0]] = 0
                    else:
                        correct_streak[quiz_queue[0][0]] += 1

                    quiz_schedule.append([quiz_queue[0][0],
                                          min(Q_DELAY[correct_streak[quiz_queue[0][0]]], len(Q_DELAY) - 1)])
                else:
                    correct_streak[quiz_queue[0][0]] = 0

            i = 0
            while i < len(quiz_schedule):
                if quiz_schedule[i][1] < 1:
                    quiz_queue.append(quiz_queue[0])
                    quiz_schedule.pop(i)
                    i -= 1
                else:
                    quiz_schedule[i][1] -= 1
                i += 1

            quiz_queue.pop(0)
            random.shuffle(quiz_queue[0][2])
            print([q[0] for q in quiz_queue], quiz_schedule)

        if timer != -1:
            if settings['mode'] == 'choice':
                y = 300
                height = size[1] // 20

                for option in quiz_queue[0][2]:
                    c = (0, 0, 0)
                    if timer == 0:
                        if y <= mouse_pos[1] <= y + height:
                            c = (50, 50, 50)
                            if mouse_click[0]:
                                c = (100, 100, 100)
                                guess(option)

                    pygame.draw.rect(screen, c, (0, y, size[0], height))

                    pygame.draw.rect(screen, (255, 255, 255), (0, y, size[0], height), 1)
                    screen.blit(font.render(option, True, (255, 255, 255)), (0, y))

                    y += height + 5
            else:
                screen.blit(font.render(typing + '|', True, (255, 255, 255)), (100, 200))
        elif timer == -1:
            screen.blit(font.render(quiz_queue[0][1], True, (100, 255, 100)), (100, 200))

        if timer > 0:
            timer -= 1
    elif state == 'editor':
        if editing[0]:
            if editing[1]:
                for i in range(2):
                    cursor = ''
                    if editing[0] == i + 1:
                        if frame // 30 % 2 == 0:
                            cursor = '_'
                    screen.blit(font.render(editing[1][i] + cursor, True, (255, 255, 255)), (100, 100 + i * 100))

    pygame.display.update()
    pre_mouse_press = mouse_press
    frame += 1

pygame.quit()
