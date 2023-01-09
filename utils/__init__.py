import utils.greekUtils

import string


class String:
    def __init__(self):
        self.lang = 'L'
        self.typing = []

    def type(self, c):
        if self.lang == 'L':
            self.typing.append(c)
        elif self.lang == 'G':
            if c == ' ':
                self.typing.append(' ')
            elif c == '(' and type(self.typing[-1]) == greekUtils.Letter:
                self.typing[-1].mod.spiritus = 1
                return
            elif c == ')' and type(self.typing[-1]) == greekUtils.Letter:
                self.typing[-1].mod.spiritus = -1
                return
            elif c == '/' and type(self.typing[-1]) == greekUtils.Letter:
                self.typing[-1].mod.acutus = 1
                return
            elif c == '\\' and type(self.typing[-1]) == greekUtils.Letter:
                self.typing[-1].mod.acutus = -1
                return
            elif c == '=' and type(self.typing[-1]) == greekUtils.Letter:
                self.typing[-1].mod.circumflex = True
                return
            elif c == '|' and type(self.typing[-1]) == greekUtils.Letter:
                self.typing[-1].mod.iota = True
                return

            elif c == ';':
                self.lang = 'L'
                self.typing.append(';')
                return

            if c.lower() not in greekUtils.greek:
                return

            # if c in string.ascii_uppercase:
            #     c = greekUtils.Letter(c.lower())
            # else:
            #     c = greekUtils.Letter(c)

            c = greekUtils.Letter(c)

            self.typing.append(c)

    def change_lang(self, lang):
        if lang not in 'LG':
            raise TypeError(f"'{lang}' not a supported language")

        self.lang = lang

    def unicode(self):
        out = ''
        i = 0
        for c in self.typing:
            if type(c) == greekUtils.Letter:
                u = c.unicode()
                if u == 'σ':
                    if i == len(self.typing) - 1:
                        out += 'ς'
                    elif type(self.typing[i + 1]) == str:
                        if self.typing[i + 1] in ' ;/,\n':
                            out += 'ς'
                        else:
                            out += 'σ'
                    else:
                        out += 'σ'
                else:
                    out += u
            elif type(c) == str:
                out += c
            i += 1

        return out
