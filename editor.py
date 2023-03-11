import utils

import pygame
pygame.init()

SPACING = 50

screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
size = screen.get_size()
font = pygame.font.Font('font/ubuntu.ttf', size[1] // 30)


def draw():
    global screen, font, typing

    for c in typing.typing:
        pass


greek = {
    'a': 'αΑ',
    'b': 'βΒ',
    'g': 'γΓ',
    'd': 'δΔ',
    'e': 'εΕ',
    'z': 'ζΖ',
    'h': 'ηΗ',
    'q': 'θΘ',  # the second one is capital here too
    'i': 'ιΙ',
    'k': 'κΚ',
    'l': 'λΛ',
    'm': 'μΜ',
    'n': 'νΝ', 'v': 'νΝ',
    'c': 'ξΖ',
    'o': 'οΟ',
    'p': 'πΠ',
    'r': 'ρΡ',
    's': 'σΣ',
    't': 'τΤ',
    'u': 'υΥ',
    'f': 'φΠ',
    'x': 'χΧ',
    'y': 'ψΨ',
    'w': 'ωΩ'
}


out = []

typing = utils.String()
lang = 'L'

pre = utils.String()

run = True
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            size = screen.get_size()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # TODO: make this a function
                split = [[]]
                i = 0
                for c in typing.typing:
                    if c != ';':
                        split[-1].append(c)
                    else:
                        split.append([])
                        split[-1] += typing.typing[i + 1:]
                        break
                    i += 1
                if len(split) == 2:
                    for i in range(len(split)):
                        for j in range(len(split[i])):
                            if type(split[i][j]) == utils.greekUtils.Letter:
                                split[i][j] = split[i][j].unicode()
                        split[i] = ''.join(split[i])
                    print(split)
                    out.append(split)
                    pre = typing
                    typing = utils.String()
            elif event.key == pygame.K_BACKSPACE:
                typing.typing = typing.typing[:-1]
            elif event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_l:
                    typing.change_lang('L')
                elif event.key == pygame.K_g:
                    typing.change_lang('G')
            else:
                typing.type(event.unicode)

    screen.blit(font.render(typing.unicode() + '|', True, (255, 255, 255)), (0, 0))
    screen.blit(font.render(pre.unicode(), True, (255, 255, 255)), (0, SPACING))

    screen.blit(font.render(typing.lang, True, (255, 255, 255)), (size[0] - SPACING, size[1] - SPACING))

    pygame.display.update()

pygame.quit()

filename = 'quizzes/' + input('filename quizzes/')
with open(filename, 'w') as file:
    out_string = '[\n\t'
    for q in out:
        out_string += '["' + q[0] + '", "' + q[1] + '"],\n\t'
    # file.write(str(out).replace("'", '"'))
    file.write(out_string[:-3] + '\n]')
