import typing
import string

# α ἀ ἁ ὰ ά ᾶ ἂ  ἃ  ἄ  ἅ  ἆ  ἇ
#   ) ( \ / = )\ (\ )/ (/ )= (=
# 0 1 2 3 4 5 6  7  8  9  10 11


class Lut:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            raw = file.read()
        self.data = raw.split('\n')

        self.dict = {}
        for line in self.data:
            if not line:
                continue
            self.dict[line[0]] = line

    def __getitem__(self, item):
        if type(item[0]) == int:
            return self.data[item[1]][item[0]]
        elif type(item[0]) == str:
            if item[0] in self.dict:
                return self.dict[item[0]][item[1]]


class Mod:
    def __init__(self):
        self.spiritus = 0  # -1 lenis/asper 1
        self.acutus = 0  # -1 acutus/gravis 1
        self.circumflex = False
        self.iota = False

    def __setattr__(self, key, value):
        if key == 'spiritus':
            if value in [-1, 0, 1]:
                self.__dict__['spiritus'] = value
        elif key == 'acutus':
            if value in [-1, 0, 1]:
                self.__dict__['acutus'] = value
                self.__dict__['circumflex'] = False
        elif key == 'circumflex':
            self.__dict__['circumflex'] = value
            self.__dict__['acutus'] = 0
        elif key == 'iota':
            self.__dict__['iota'] = value
        else:
            raise AttributeError(f'{key} not in {self}')

    def unicode(self):
        return


greek = {
    'a': 'αΑ', 'b': 'βΒ', 'g': 'γΓ', 'd': 'δΔ', 'e': 'εΕ', 'z': 'ζΖ', 'h': 'ηΗ', 'q': 'θΘ', 'i': 'ιΙ', 'k': 'κΚ',
    'l': 'λΛ', 'm': 'μΜ', 'n': 'νΝ', 'c': 'ξΖ', 'o': 'οΟ', 'p': 'πΠ', 'r': 'ρΡ', 's': 'σΣ', 't': 'τΤ', 'u': 'υΥ',
    'f': 'φΠ', 'x': 'χΧ', 'y': 'ψΨ', 'w': 'ωΩ', 'v': 'νΝ'
}


class Letter:
    def __init__(self, char, mod=None, filename='G_LUT.txt'):
        if char in string.ascii_lowercase:
            self.char = greek[char][0]
        else:
            self.char = greek[char.lower()][1]

        if mod is not None:
            self.mod = mod
        else:
            self.mod = Mod()

        self.LUT = Lut(filename)

    def unicode(self):
        if self.char not in self.LUT.dict:
            return self.char

        n = 0

        if self.mod.spiritus == -1:
            if self.mod.acutus == -1:
                n = 6
            elif self.mod.acutus == 1:
                n = 8
            elif self.mod.circumflex:
                n = 10
            else:
                n = 1
        elif self.mod.spiritus == 1:
            if self.mod.acutus == -1:
                n = 7
            elif self.mod.acutus == 1:
                n = 9
            elif self.mod.circumflex:
                n = 11
            else:
                n = 2
        else:
            if self.mod.acutus == -1:
                n = 3
            elif self.mod.acutus == 1:
                n = 4
            elif self.mod.circumflex:
                n = 5
            else:
                n = 0

        n += 12 * self.mod.iota

        return self.LUT[self.char, n]


class GreekStr:
    def __init__(self, data: str):
        """
        creates a string for ancient greek
        :param data: str of latin characters to be converted to ancient greek characters
        """
        self.data = []
        self + data

    def __repr__(self) -> str:
        return ''.join([letter.unicode() for letter in self.data])

    def __add__(self, other):
        if type(other) == GreekStr:
            self.data += other
        elif type(other) == str:
            for c in other:
                self.data.append(Letter(c))
        else:
            raise TypeError('GreekStr')


if __name__ == '__main__':
    s = GreekStr('test')
    print(s)

    # TODO: add tests
