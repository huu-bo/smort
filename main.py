#!/usr/bin/python3

import json
import enum
import pygame
import random
import os
from difflib import SequenceMatcher

from host import host
from utils.greekUtils import translit
pygame.init()

# choose by clicking,
# you can use 1, 2, 3, 4 buttons in the player

# big word/words is/are the question(s)
# number in top right is % correctness

# TODO: different font (circumflex broken)

size = (800, 800)
settings = {
    'mode': 'choice'  # choice, type, game
}
DELAY = 2  # should be more than 1
RATIO_CORRECT = .7
GAME_TIME = 180
GAME_PLAYER_SPEED = .008

state = 'main'  # main, practice, practice_settings

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
quiz_queue = []

timer = 0
last_correct = False
typing = ''

q_selection = 0
q_ret = False

correct = [0., {}]

game_cam = 0
game_player = 0
game_time = GAME_TIME


def practice(f):
    global quiz, quiz_queue, state, timer, correct
    with open(f, 'r', encoding='UTF-8') as file:
        quiz = json.load(file)

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

    state = 'practice'
    timer = 0


def game():
    if settings['mode'] != 'game':
        raise ValueError

    global game_cam, game_player, game_time
    game_cam = .3
    game_player = .5
    game_time = GAME_TIME


def new_learn():
    global quiz, quiz_queue, correct

    not_correct = [i for i, _, _ in quiz if i not in correct[1]]
    if len(not_correct) == 0:
        print('user has been shown all')
        quiz_queue.append(random.choice(quiz))
    else:
        i = random.choice(not_correct)
        for q in quiz:
            if q[0] == i:
                quiz_queue.append(q)
                break
        else:
            raise IndexError(f"index '{i}' not in quiz")


def guess(option):
    global quiz_queue, timer, last_correct, settings, quiz, DELAY, correct
    if option == quiz_queue[0][1]:
        timer = DELAY
        last_correct = True
    else:
        timer = -1
        last_correct = False

        if option:
            for q in quiz:
                if q != quiz_queue[0]:
                    if option in q[1]:
                        quiz_queue.append(q)  # add all questions that also have the answer that you gave

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


def draw_files(qs, y: int, level: int, selected: int, ret: bool):
    mod = pygame.key.get_mods()
    height = size[1] // 20

    for q in qs:
        # print(q)
        c = (0, 0, 0)
        if y <= mouse_pos[1] <= y + height:
            c = (50, 50, 50)
            if mouse_click[0]:
                c = (100, 100, 100)
                if not q[QS.FOLDER]:
                    practice(q[QS.FILE_NAME])
                else:
                    q[QS.FOLDER_SELECTED] = not q[QS.FOLDER_SELECTED]
        if selected == y // height:
            c = (50, 50, 50)
            if ret:
                c = (100, 100, 100)
                if not q[QS.FOLDER]:
                    if mod & pygame.KMOD_SHIFT:
                        host_(q, False)
                    else:
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


def host_(q, t: bool):
    body = ''
    body += '<table>'
    with open(q[QS.FILE_NAME], 'r', encoding='utf-8') as file:
        raw = json.load(file)
        for row in raw:
            body += '<tr>'
            for i in range(2):
                body += f'<td>{row[i]}</td>'
                if i == 0 and t:
                    body += f'<td>{translit(row[i])}</td>'
            body += '</tr>'
    body += '</table>'
    head = '<style>tr:nth-child(even) {background-color: #f2f2f2} td {padding: 8px}</style>'
    host.host('localhost', 8080,
              host.get_html(q[QS.DRAW_NAME], body, head=head))


mouse_scroll = 0

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

        elif event.type == pygame.MOUSEWHEEL:
            mouse_scroll += event.precise_y

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

                    if event.key == pygame.K_m:
                        settings['mode'] = 'type'
                    if event.key == pygame.K_g:
                        settings['mode'] = 'game'
                        game()

                elif settings['mode'] == 'type':
                    if event.key == pygame.K_RETURN and timer == 0:
                        guess(typing)
                        typing = ''
                    elif event.key == pygame.K_BACKSPACE:
                        typing = typing[:-1]
                    elif event.key == pygame.K_m and event.mod & pygame.KMOD_CTRL:
                        settings['mode'] = 'choice'
                    else:
                        typing += event.unicode

                elif settings['mode'] == 'game':
                    pass

                else:
                    assert False, settings['mode']

                if event.key == pygame.K_ESCAPE:
                    state = 'main'
            elif state == 'main':
                if event.key == pygame.K_DOWN:
                    q_selection += 1
                elif event.key == pygame.K_UP:
                    if q_selection > 0:
                        q_selection -= 1
                if event.key == pygame.K_RETURN:
                    q_ret = True

                kmod = pygame.key.get_mods()
                if event.key == pygame.K_SPACE and kmod & pygame.KMOD_CTRL and kmod & pygame.KMOD_SHIFT:
                    font = pygame.font.Font('font/ubuntu.ttf', size[1] // 30)
                    big_font = pygame.font.Font('font/ubuntu.ttf', size[1] // 20)
                elif event.key == pygame.K_SPACE and kmod & pygame.KMOD_CTRL:
                    font = pygame.font.Font('font/NotoSansJP-Regular.otf', size[1] // 30)
                    big_font = pygame.font.Font('font/NotoSansJP-Regular.otf', size[1] // 20)

            else:
                raise AssertionError(f"unknown state '{state}'")

    mouse_pos = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed(3)
    mouse_click = [mouse_press[i] and not pre_mouse_press[i] for i in range(3)]

    if state == 'main':
        draw_files(qs, mouse_scroll, 0, q_selection, q_ret)

    elif state == 'practice':
        if not quiz_queue:
            new_learn()

        screen.blit(big_font.render(quiz_queue[0][0], True, (255, 255, 255)), (100, 100))
        screen.blit(font.render(str(round(correct[0] * 100)), True, (255, 255, 255)), (size[0] - 70, 50))

        if timer == 1:
            if len(quiz_queue) > 2 - last_correct:
                pass
            else:
                new_learn()

            if not last_correct:
                quiz_queue.insert(2, quiz_queue[0])

            quiz_queue.pop(0)
            random.shuffle(quiz_queue[0][2])
            print([q[0] for q in quiz_queue])

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

            elif settings['mode'] == 'type':
                screen.blit(font.render(typing + '|', True, (255, 255, 255)), (100, 200))

            elif settings['mode'] == 'game':
                width = screen.get_width() / len(quiz_queue[0][2])
                height = big_font.get_height()
                x = 0
                y = game_cam * screen.get_height()
                for choice in quiz_queue[0][2]:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, 1, height))
                    screen.blit(font.render(choice, True, (255, 255, 255)), (x, y))
                    x += width

                game_cam += 1 / game_time

                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    game_player -= GAME_PLAYER_SPEED
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    game_player += GAME_PLAYER_SPEED

                if game_player < 0:
                    game_player = 0
                if game_player >= 1:
                    game_player = 1

                px = game_player * screen.get_width()
                py = screen.get_height() - height
                pygame.draw.rect(screen, (255, 255, 255), (px, py, 1, height))

                if game_cam >= 1:
                    g = quiz_queue[0][2][int(px // width)]
                    guess(g)
                    game_cam = 0

                    if last_correct:
                        game_time -= 10
                    else:
                        game_time += 10
                    print(game_time)

            else:
                assert False, settings['mode']

        elif timer == -1:
            screen.blit(font.render(quiz_queue[0][1], True, (100, 255, 100)), (100, 200))

        if timer > 0:
            timer -= 1

    else:
        raise AssertionError(f"unknown state '{state}'")

    pygame.display.update()
    pre_mouse_press = mouse_press
    frame += 1

pygame.quit()
