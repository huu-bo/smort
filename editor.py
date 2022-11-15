import string
import greekUtils as gu


# https://stackoverflow.com/a/21659588
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys
    import tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()


def print_g():
    global typing
    print('\r' + ' ' * 80 + '\r', end='')
    i = 0
    for c in typing:
        if type(c) != gu.Letter:
            if c == 'σ':
                if i < len(typing) - 1:
                    if typing[i + 1] not in ' \n;':
                        print(c, end='')
                    else:
                        print('ς', end='')
                else:
                    print('ς', end='')
            else:
                print(c, end='')
        else:
            u = c.unicode()
            if u == 'σ' and len(typing) - 1 > i:
                if type(typing[i + 1]) == gu.Letter:
                    print(u, end='')
                    continue
                if typing[i + 1] not in ' \n;':
                    print(u, end='')
                else:
                    print('ς', end='')
            else:
                print(c.unicode(), end='')
        i += 1


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
    'n': 'νΝ',
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
lang = 'L'
typing = []
c = 'T'
while True:
    c = getch()

    if hex(ord(c)) == '0x3':  # ^C
        break
    elif hex(ord(c)) == '0xd':  # newline
        split = [[]]
        i = 0
        for c in typing:
            if c != ';':
                split[-1].append(c)
            else:
                split.append([])
                split[-1] += typing[i+1:]
                break
            i += 1
        if len(split) == 2:
            out_ss = []
            for s in split:
                out_s = []
                for c in s:
                    if type(c) == gu.Letter:
                        u = c.unicode()
                        if u == 'σ' and len(typing) + 1 < i:
                            if typing[i + 1] not in ' \n;':  # does not work with gu.Letter but shouldn't matter
                                out_s.append(u)
                            else:
                                out_s.append('ς')
                        else:
                            out_s.append(u)
                    else:
                        out_s.append(c)
                out_ss.append(''.join(out_s))
            # if len(out_ss) > 2:
            #     i = 2
            #     print(out_ss)
            #     while i < len(out_ss):
            #         out_ss[1] = out_ss[1].join(out_ss.pop(i))
            #         print(out_ss)
            #         # i += 1
            out.append(out_ss)

        typing = []
        print_g()
        continue
    elif hex(ord(c)) == '0x7f':  # backspace
        typing = typing[:-1]
        print_g()
        continue
    elif c == ' ':
        typing += ' '
        print_g()
        continue

    elif c == 'G':
        lang = 'G'
        continue
    elif c == 'L':
        lang = 'L'
        continue

    elif c == '(' and type(typing[-1]) == gu.Letter:
        typing[-1].mod.spiritus = 1
        print_g()
        continue
    elif c == ')' and type(typing[-1]) == gu.Letter:
        typing[-1].mod.spiritus = -1
        print_g()
        continue
    elif c == '/' and type(typing[-1]) == gu.Letter:
        typing[-1].mod.acutus = 1
        print_g()
        continue
    elif c == '\\' and type(typing[-1]) == gu.Letter:
        typing[-1].mod.acutus = -1
        print_g()
        continue
    elif c == '=' and type(typing[-1]) == gu.Letter:
        typing[-1].mod.circumflex = True
        print_g()
        continue
    elif c == '|' and type(typing[-1]) == gu.Letter:
        typing[-1].mod.iota = True
        print_g()
        continue

    elif c == ';':
        lang = 'L'

    # else:
    #     print(hex(ord(c)))

    if lang == 'G':
        if c.lower() not in greek:
            continue

        if c in string.ascii_uppercase:
            c = gu.Letter(c.lower())
        else:
            c = gu.Letter(c)

    typing.append(c)
    print_g()

print()
print(str(out).replace("'", '"'))

filename = 'quizzes/ARGO grieks/' + input('filename quizzes/ARGO grieks/')

with open(filename, 'w') as file:
    file.write(str(out).replace("'", '"'))
