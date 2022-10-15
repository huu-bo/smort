import pygame


class gui:
    def __init__(self, screen: pygame.Surface):
        self.size = screen.get_size()
        self.screen = screen
        self.elements = []
        self.font = pygame.font.SysFont('ubuntu', size=self.size[1] // 40)

        self.pre_mouse_press = (False, False, False)

    def render(self, mouse_pos, mouse_press):
        mouse_click = [mouse_press[i] and not self.pre_mouse_press[i] for i in range(3)]

        self.screen.fill((0, 0, 0))

        for e in self.elements:
            rect = self.rect(e.p)
            if e.render is None:
                c = (0, 0, 200)
                if rect[0] <= mouse_pos[0] <= rect[0] + rect[2]:
                    if rect[1] <= mouse_pos[1] <= rect[1] + rect[3]:
                        if mouse_click[0]:
                            c = (200, 200, 255)
                            if e.function is not None:
                                e.function()
                        else:
                            c = (0, 0, 255)

                pygame.draw.rect(self.screen, c, rect)
                self.screen.blit(self.font.render(e.text, True, (255, 255, 255)), (rect[0], rect[1]))
            else:
                e.render(self, rect, mouse_pos, mouse_press, mouse_click)

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.type == pygame.KEYDOWN:
                for e in self.elements:
                    if event.unicode == e.keybind:
                        e.function()

        self.pre_mouse_press = mouse_press

    def add(self, e):
        self.elements.append(e)

    def remove(self, e):
        if e in self.elements:
            self.elements.remove(e)

    def rect(self, p):
        return int(p[0] / p[1] * self.size[0]), int(p[2] / p[3] * self.size[1]),\
               int(self.size[0] / p[1]), int(self.size[1] / p[3])


class element:
    def __init__(self, p: tuple, text, function=None, render=None, keybind=None):
        if type(p) is not tuple or len(p) != 4:
            raise TypeError('p of element should be a tuple of length 4')

        self.p = p
        self.text = text
        self.keybind = keybind

        self.function = function
        self.render = render
