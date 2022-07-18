import pygame as pg
import os
import main

pg.font.init()

# define the window surface as the one used in main (in this case, 'WIN')
win = main.WIN

counter_list = []


class counter:

    def __init__(self, x, y, size, value=0, title="", title_size=14):
        if title != "":
            self.title = title
            self.title_font = pg.font.SysFont('arial', title_size)
            # title font color must be changed manualy through assignment, not included in function
            self.title_font_color = (16, 16, 16)
            self.title_render = self.title_font.render(
                str(title), 1, self.title_font_color)
            self.title_render_x, self.title_render_y = x, y - \
                self.title_render.get_height() - (size * 0.05)

        self.font = pg.font.SysFont('arial', size)
        # font color must be changed manualy through assignment, not included in function
        self.font_color = (0, 0, 0)
        self.value = value
        self.value_render = self.font.render(str(value), 1, self.font_color)
        self.value_render_x, self.value_render_y = size * 1.1 + \
            x, y - ((self.value_render.get_height() - size) / 2)

        self.minus = pg.transform.scale(pg.image.load(
            os.path.join('Assets', 'Minus.png')), (size, size))
        self.minus_rect = pg.Rect(x, y, size, size)
        self.plus = pg.transform.scale(pg.image.load(
            os.path.join('Assets', 'Plus.png')), (size, size))
        self.plus_rect = pg.Rect(
            x + (size * 1.2) + self.value_render.get_width(), y, size, size)

        # position and dimensions do not include title
        self.x, self.y = x, y
        self.width, self.height = x + \
            (size * 2.2) + self.value_render.get_width(), size
        self.size = size

        counter_list.append(self)

    def draw(self):
        if self.title != "":
            win.blit(self.title_render,
                     (self.title_render_x, self.title_render_y))

        win.blit(self.minus, (self.minus_rect.x, self.minus_rect.y))
        win.blit(self.value_render, (self.value_render_x, self.value_render_y))
        win.blit(self.plus, (self.plus_rect.x, self.plus_rect.y))

    def update():
        for counter in counter_list:
            if counter.title != "":
                counter.title_render = counter.title_font.render(
                    str(counter.title), 1, counter.title_font_color)
                counter.title_render_x, counter.title_render_y = counter.x, counter.y - \
                    counter.title_render.get_height() - (counter.size * 0.05)

            counter.value_render = counter.font.render(
                str(counter.value), 1, counter.font_color)
            counter.value_render_x, counter.value_render_y = counter.size * 1.1 + \
                counter.x, counter.y - \
                ((counter.value_render.get_height() - counter.size) / 2)
            counter.minus_rect.x, counter.minus_rect.y = counter.x, counter.y
            counter.plus_rect.x, counter.plus_rect.y = counter.x + \
                (counter.size * 1.2) + counter.value_render.get_width(), counter.y

            counter.width = counter.x + \
                (counter.size * 2.2) + counter.value_render.get_width()
