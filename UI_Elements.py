from turtle import width
import pygame as pg
import os
import main

pg.font.init()

# define the window surface as the one used in main (in this case, 'WIN')
win = main.WIN

counter_list = []


class Counter:

    def __init__(self, x: int, y: int, size: int, value: int = 0, title: str = "", title_size: int = 14):
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
        self.width, self.height = (size * 2.2) + \
            self.value_render.get_width(), size
        self.size = size

        counter_list.append(self)

    def draw(self):
        if self.title != "":
            win.blit(self.title_render,
                     (self.title_render_x, self.title_render_y))

        win.blit(self.minus, (self.minus_rect.x, self.minus_rect.y))
        win.blit(self.value_render, (self.value_render_x, self.value_render_y))
        win.blit(self.plus, (self.plus_rect.x, self.plus_rect.y))

    def handleInput():
        mouse_pos = pg.mouse.get_pos()
        for c in counter_list:
            if c.minus_rect.collidepoint(mouse_pos):
                c.value -= 1
            if c.plus_rect.collidepoint(mouse_pos):
                c.value += 1

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

            counter.width = (counter.size * 2.2) + \
                counter.value_render.get_width()


class BorderRect:
    def __init__(self, x: int, y: int, width: int, height: int, thickness: int):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.thickness = thickness

    def draw(self, surface: pg.Surface, color: tuple, border_color: tuple):
        border = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, border_color, border)
        pg.draw.rect(surface, color, pg.Rect(self.thickness + self.x, self.thickness + self.y,
                     self.width - (self.thickness * 2), self.height - (self.thickness * 2)))


class Dropdown:
    dropdown_list = []

    def __init__(self, x: int, y: int, width: int, height: int, options: list, title: str = "", title_size: int = 14):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.options = options
        self.selected_num = -1
        self.selected_str = ""
        self.opened = False

        self.border_thickness = 4
        self.inner_border_thickness = self.border_thickness // 2
        self.border_color = (0, 0, 0)
        self.background_color = (255, 255, 255)

        self.font = pg.font.SysFont(
            'arial', height - (self.border_thickness * 2))
        self.font_color = (0, 0, 0)
        self.option_renders = []
        for option in options:
            self.option_renders.append(
                self.font.render(option, 1, self.font_color))

        self.arrow = pg.transform.scale(pg.image.load(os.path.join('Assets', 'dropdown.png')), ((
            height - (self.border_thickness * 2)) // 2, height - (self.border_thickness * 2)))

        self.title = title
        self.title_size = title_size
        self.title_color = (0, 0, 0)
        self.title_font = pg.font.SysFont('arial', self.title_size)
        self.title_render = self.title_font.render(title, 1, self.title_color)

        Dropdown.dropdown_list.append(self)

    def draw(self):
        if self.title != "":
            self.title_render = self.title_font.render(
                self.title, 1, self.title_color)
            win.blit(self.title_render, (self.x, self.y -
                     self.title_render.get_height() - (self.height * 0.05)))

        BorderRect(self.x, self.y, self.width, self.height, self.border_thickness).draw(
            win, self.background_color, self.border_color)
        if self.selected_num != -1:
            selected_render = self.option_renders[self.selected_num]
            win.blit(selected_render, (self.x + self.border_thickness + (selected_render.get_height() * 0.1), self.y), (0,
                     (selected_render.get_height() - self.height) / 2, self.width - (self.border_thickness + (selected_render.get_height() * 0.1)), self.height))
        i = 1
        i2 = 0

        # abandon all hope, ye who enter here
        if self.opened:
            for option in self.options:
                if option != self.selected_str:
                    pg.draw.rect(win, self.border_color, pg.Rect(
                        self.x, self.y + (self.height * i), self.width, self.height))
                    pg.draw.rect(win, self.background_color, pg.Rect(self.x + self.inner_border_thickness, self.y + (
                        self.height * i), self.width - (self.inner_border_thickness * 2), self.height - self.inner_border_thickness))
                    win.blit(self.option_renders[i2], (self.x + self.inner_border_thickness + (self.option_renders[i2].get_height() * 0.1), self.y + (
                        self.height * i)), (0, (self.option_renders[i2].get_height() - self.height) / 2, self.width - (self.inner_border_thickness + (self.option_renders[i2].get_height() * 0.1)), self.height))
                    i += 1
                i2 += 1
            win.blit(pg.transform.rotate(self.arrow, 180), (self.x + self.width -
                     self.border_thickness - self.arrow.get_width(), self.y + self.border_thickness))
        else:
            win.blit(self.arrow, (self.x + self.width - self.border_thickness -
                     self.arrow.get_width(), self.y + self.border_thickness))

    def update():
        for dropdown in Dropdown.dropdown_list:
            if dropdown.selected_num == -1:
                dropdown.selected_str = ""
            else:
                dropdown.selected_str = dropdown.options[dropdown.selected_num]
            dropdown.option_renders = []
            for option in dropdown.options:
                dropdown.option_renders.append(
                    dropdown.font.render(option, 1, dropdown.font_color))
            dropdown.title_render = dropdown.title_render = dropdown.title_font.render(
                dropdown.title, 1, dropdown.title_color)

    def handleInput():
        mouse_pos = pg.mouse.get_pos()
        for dropdown in Dropdown.dropdown_list:
            if pg.Rect(dropdown.x, dropdown.y, dropdown.width, dropdown.height).collidepoint(mouse_pos):
                dropdown.opened = not dropdown.opened
            if dropdown.opened:
                for i in range(1, len(dropdown.options) - (not not (dropdown.selected_num + 1)) + 1):
                    if pg.Rect(dropdown.x, dropdown.y + (i * dropdown.height), dropdown.width, dropdown.height).collidepoint(mouse_pos):
                        if dropdown.selected_num == -1:
                            dropdown.selected_num = i - 1
                        else:
                            if i - 1 < dropdown.selected_num:
                                dropdown.selected_num = i-1
                            else:
                                dropdown.selected_num = i
                        dropdown.opened = not dropdown.opened


class Checkmark:
    checkmark_list = []

    def __init__(self, x: int, y: int, title: str, size: int, check_placement: str = 'l'):
        assert check_placement in [
            'u', 'd', 'l', 'r'], 'check_placement parameter must be u, d, l, r'
        self.check_placement = check_placement

        self.x, self.y = x, y
        self.size = size

        self.title = title
        self.title_color = (0, 0, 0)
        self.size = size
        self.title_font = pg.font.SysFont('arial', size)
        self.title_render = self.title_font.render(title, 1, self.title_color)

        self.box_thickness = 4
        self.check_placement = check_placement
        if self.check_placement == 'u':
            self.box = BorderRect(
                x + (self.title_render.get_width() / 2) - (size / 2), y, size, size, self.box_thickness)
        elif self.check_placement == 'd':
            self.box = BorderRect(x + (self.title_render.get_width() / 2) - (size / 2), y +
                                  self.title_render.get_height(), size, size, self.box_thickness)
        elif self.check_placement == 'l':
            self.box = BorderRect(
                x, y + ((self.title_render.get_height() - size) / 2), size, size, self.box_thickness)
        elif self.check_placement == 'r':
            self.box = BorderRect(x + self.title_render.get_width() + (size * 0.05), y + (
                (self.title_render.get_height() - size) / 2), size, size, self.box_thickness)
        self.box_color = (255, 255, 255)
        self.box_border_color = (0, 0, 0)

        self.value = False
        self.check = pg.transform.scale(pg.image.load(os.path.join(
            'Assets', 'check.png')), (size - (self.box_thickness * 2), size - (self.box_thickness * 2)))

        Checkmark.checkmark_list.append(self)

    def draw(self):
        self.box.draw(win, self.box_color, self.box_border_color)
        if self.value:
            win.blit(self.check, (self.box.x + self.box_thickness,
                     self.box.y + self.box_thickness))

        if self.check_placement == 'u':
            win.blit(self.title_render, (self.x, self.y + self.size))
        elif self.check_placement == 'd':
            win.blit(self.title_render, (self.x, self.y))
        elif self.check_placement == 'l':
            win.blit(self.title_render, (self.x + (self.size * 1.05), self.y))
        elif self.check_placement == 'r':
            win.blit(self.title_render, (self.x, self.y))

    def handleInput():
        mouse_pos = pg.mouse.get_pos()
        for c in Checkmark.checkmark_list:
            if pg.Rect(c.box.x, c.box.y, c.size, c.size).collidepoint(mouse_pos):
                c.value = not c.value

    def update():
        for c in Checkmark.checkmark_list:
            c.title_font = pg.font.SysFont('arial', c.size)
            c.title_render = c.title_font.render(c.title, 1, c.title_color)
            c.box.thickness = c.box_thickness
            c.check = pg.transform.scale(
                c.check, (c.size - (c.box_thickness * 2), c.size - (c.box_thickness * 2)))
