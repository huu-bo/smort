import utils

import pygame
pygame.init()

SPACING = 50

screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
size = screen.get_size()
font = pygame.font.Font('font/ubuntu.ttf', size[1] // 30)


# def print_g():
#     global typing
#     print('\r' + ' ' * 80 + '\r', end='')
#     i = 0
#     for c in typing:
#         if type(c) != gu.Letter:
#             if c == 'σ':
#                 if i < len(typing) - 1:
#                     if typing[i + 1] not in ' \n;':
#                         print(c, end='')
#                     else:
#                         print('ς', end='')
#                 else:
#                     print('ς', end='')
#             else:
#                 print(c, end='')
#         else:
#             u = c.unicode()
#             if u == 'σ' and len(typing) - 1 > i:
#                 if type(typing[i + 1]) == gu.Letter:
#                     print(u, end='')
#                     continue
#                 if typing[i + 1] not in ' \n;':
#                     print(u, end='')
#                 else:
#                     print('ς', end='')
#             else:
#                 print(c.unicode(), end='')
#         i += 1


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

# out = []
# lang = 'L'
# typing = []
# c = 'T'
# while True:
#     c = getch()
#
#     if hex(ord(c)) == '0x3':  # ^C
#         break
#     elif hex(ord(c)) == '0xd':  # newline
#         split = [[]]
#         i = 0
#         for c in typing:
#             if c != ';':
#                 split[-1].append(c)
#             else:
#                 split.append([])
#                 split[-1] += typing[i+1:]
#                 break
#             i += 1
#         if len(split) == 2:
#             out_ss = []
#             for s in split:
#                 out_s = []
#                 for c in s:
#                     if type(c) == gu.Letter:
#                         u = c.unicode()
#                         if u == 'σ' and len(typing) + 1 < i:
#                             if typing[i + 1] not in ' \n;':  # does not work with gu.Letter but shouldn't matter
#                                 out_s.append(u)
#                             else:
#                                 out_s.append('ς')
#                         else:
#                             out_s.append(u)
#                     else:
#                         out_s.append(c)
#                 out_ss.append(''.join(out_s))
#             # if len(out_ss) > 2:
#             #     i = 2
#             #     print(out_ss)
#             #     while i < len(out_ss):
#             #         out_ss[1] = out_ss[1].join(out_ss.pop(i))
#             #         print(out_ss)
#             #         # i += 1
#             out.append(out_ss)
#
#         typing = []
#         print_g()
#         continue
#     elif hex(ord(c)) == '0x7f':  # backspace
#         typing = typing[:-1]
#         print_g()
#         continue
#     elif c == ' ':
#         typing += ' '
#         print_g()
#         continue
#
#     elif c == 'G':
#         lang = 'G'
#         continue
#     elif c == 'L':
#         lang = 'L'
#         continue
#
#     elif c == '(' and type(typing[-1]) == gu.Letter:
#         typing[-1].mod.spiritus = 1
#         print_g()
#         continue
#     elif c == ')' and type(typing[-1]) == gu.Letter:
#         typing[-1].mod.spiritus = -1
#         print_g()
#         continue
#     elif c == '/' and type(typing[-1]) == gu.Letter:
#         typing[-1].mod.acutus = 1
#         print_g()
#         continue
#     elif c == '\\' and type(typing[-1]) == gu.Letter:
#         typing[-1].mod.acutus = -1
#         print_g()
#         continue
#     elif c == '=' and type(typing[-1]) == gu.Letter:
#         typing[-1].mod.circumflex = True
#         print_g()
#         continue
#     elif c == '|' and type(typing[-1]) == gu.Letter:
#         typing[-1].mod.iota = True
#         print_g()
#         continue
#
#     elif c == ';':
#         lang = 'L'
#
#     # else:
#     #     print(hex(ord(c)))
#
#     if lang == 'G':
#         if c.lower() not in greek:
#             continue
#
#         if c in string.ascii_uppercase:
#             c = gu.Letter(c.lower())
#         else:
#             c = gu.Letter(c)
#
#     typing.append(c)
#     print_g()

# print()
# print(str(out).replace("'", '"'))
#
# filename = 'quizzes/ARGO grieks/' + input('filename quizzes/ARGO grieks/')
#
# with open(filename, 'w') as file:
#     file.write(str(out).replace("'", '"'))


out = []

typing = utils.String()
lang = 'L'

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
            if event.unicode:
                typing.type(event.unicode)
            elif event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_l:
                    typing.change_lang('L')
                elif event.key == pygame.K_g:
                    typing.change_lang('G')
            else:  # things like newline and backspace
                if event.key == pygame.K_RETURN:
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
                        typing = utils.String()
                elif event.key == pygame.K_BACKSPACE:
                    typing.typing = typing.typing[:-1]

    screen.blit(font.render(typing.unicode(), True, (255, 255, 255)), (0, 0))

    screen.blit(font.render(typing.lang, True, (255, 255, 255)), (size[0] - SPACING, size[1] - SPACING))

    pygame.display.update()

pygame.quit()

filename = 'quizzes/ARGO grieks/' + input('filename quizzes/ARGO grieks/')
with open(filename, 'w') as file:
    file.write(str(out).replace("'", '"'))
