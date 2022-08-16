from turtle import color
import pygame as pg
import os

pg.font.init()


def init():
    global win
    win = pg.display.get_surface()


list = []


class BorderRect:

    def __init__(self, x: float, y: float, width: float, height: float, thickness: float):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.thickness = thickness

    def draw(self, surface: pg.Surface, color: tuple, border_color: tuple):
        border = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, border_color, border)
        pg.draw.rect(surface, color, pg.Rect(self.thickness + self.x, self.thickness + self.y,
                     self.width - (self.thickness * 2), self.height - (self.thickness * 2)))


class Header:
    header_list = []

    def __init__(self, y: float, title: str, size: int, thickness: float = 2, color: tuple = (100, 100, 100), bold: bool = True):
        self.y = y
        self.thickness = thickness
        self.size = size
        self.title = title
        self.title_font = pg.font.SysFont('arial', size, bold)
        self.title_render = self.title_font.render(title, 1, color)
        self.color = color

        Header.header_list.append(self)

    def draw(self):
        pg.draw.line(win, self.color, (10, self.y), (pg.display.get_surface(
        ).get_width() - 10, self.y), self.thickness)
        win.blit(self.title_render, (10, self.y - self.size))

    def update():
        for h in Header.header_list:
            h.title_render = h.title_font.render(h.title, 1, h.color)


class Counter:
    counter_list = []

    def __init__(self, x: float, y: float, size: int, value: int = 0, title: str = "", title_size: int = 14):
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

        self.minus = pg.transform.smoothscale(pg.image.load(
            os.path.join('Assets', 'Minus.png')), (size, size))
        self.minus_rect = pg.Rect(x, y, size, size)
        self.plus = pg.transform.smoothscale(pg.image.load(
            os.path.join('Assets', 'Plus.png')), (size, size))
        self.plus_rect = pg.Rect(
            x + (size * 1.2) + self.value_render.get_width(), y, size, size)

        # position and dimensions do not include title
        self.x, self.y = x, y
        self.width, self.height = (size * 2.2) + \
            self.value_render.get_width(), size
        self.size = size

        Counter.counter_list.append(self)
        list.append(self)

    def draw(self):
        if self.title != "":
            win.blit(self.title_render,
                     (self.title_render_x, self.title_render_y))

        win.blit(self.minus, (self.minus_rect.x, self.minus_rect.y))
        win.blit(self.value_render, (self.value_render_x, self.value_render_y))
        win.blit(self.plus, (self.plus_rect.x, self.plus_rect.y))

    def handleInput(event):
        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
            mouse_pos = pg.mouse.get_pos()
            for c in Counter.counter_list:
                if c.minus_rect.collidepoint(mouse_pos):
                    c.value -= 1
                if c.plus_rect.collidepoint(mouse_pos):
                    c.value += 1

    def update():
        for counter in Counter.counter_list:
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


class Dropdown:
    dropdown_list = []

    def __init__(self, x: float, y: float, width: float, height: float, options: list, title: str = "", title_size: int = 14):
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

        self.arrow = pg.transform.smoothscale(pg.image.load(os.path.join('Assets', 'dropdown.png')), ((
            height - (self.border_thickness * 2)) // 2, height - (self.border_thickness * 2)))

        self.title = title
        self.title_size = title_size
        self.title_color = (0, 0, 0)
        self.title_font = pg.font.SysFont('arial', self.title_size)
        self.title_render = self.title_font.render(title, 1, self.title_color)

        Dropdown.dropdown_list.append(self)
        list.append(self)

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

    def handleInput(event):
        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
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


class Checkmark:
    checkmark_list = []

    def __init__(self, x: float, y: float, title: str, size: int, check_placement: str = 'l'):
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
            self.box = BorderRect(x + self.title_render.get_width() + (size * 0.2), y + (
                (self.title_render.get_height() - size) / 2), size, size, self.box_thickness)
        self.box_color = (255, 255, 255)
        self.box_border_color = (0, 0, 0)

        self.value = False
        self.check = pg.transform.smoothscale(pg.image.load(os.path.join(
            'Assets', 'check.png')), (size - (self.box_thickness * 2), size - (self.box_thickness * 2)))

        Checkmark.checkmark_list.append(self)
        list.append(self)

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
            win.blit(self.title_render, (self.x + (self.size * 1.2), self.y))
        elif self.check_placement == 'r':
            win.blit(self.title_render, (self.x, self.y))

    def handleInput(event):
        if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
            mouse_pos = pg.mouse.get_pos()
            for c in Checkmark.checkmark_list:
                if pg.Rect(c.box.x, c.box.y, c.size, c.size).collidepoint(mouse_pos):
                    c.value = not c.value

    def update():
        for c in Checkmark.checkmark_list:
            c.title_font = pg.font.SysFont('arial', c.size)
            c.title_render = c.title_font.render(c.title, 1, c.title_color)
            c.box.thickness = c.box_thickness
            c.check = pg.transform.smoothscale(
                c.check, (c.size - (c.box_thickness * 2), c.size - (c.box_thickness * 2)))
            if c.check_placement == 'u':
                c.box.y = c.y
            elif c.check_placement == 'd':
                c.box.y = c.y + c.title_render.get_height()
            elif c.check_placement == 'l':
                c.box.y = c.y + ((c.title_render.get_height() - c.size) / 2)
            elif c.check_placement == 'r':
                c.box.y = c.y + ((c.title_render.get_height() - c.size) / 2)


class TextField:
    textField_list = []

    def __init__(self, x: float, y: float, width: float, height: float, text_size: int, border_thickness: float = 4, title: str = '', title_size: str = 14):
        self.x, self.y = x, y
        self.width, self.height = width, height

        if title != '':
            self.title = title
            self.title_size = title_size
            self.title_color = (0, 0, 0)
            self.title_font = pg.font.SysFont('arial', title_size)
            self.title_render = self.title_font.render(
                title, 1, self.title_color)
            self.title_x, self.title_y = x, y - (title_size * 1.1)

        self.text_size = text_size
        self.font_color = (0, 0, 0)
        self.font = pg.font.SysFont('arial', text_size)
        self.font_height = self.font.render(
            '', 0, (0, 0, 0), (0, 0, 0)).get_height()
        self.renders = []
        self.content = ['']

        self.border_thickness = border_thickness
        self.box = BorderRect(x, y, width, height, border_thickness)
        self.color = (255, 255, 255)
        self.unselected_color = (128, 128, 128)
        self.selected_color = (0, 0, 0)
        self.selected = False

        self.cursor_color = (0, 0, 0)
        self.cursor_off_x, self.cursor_off_y = self.x + self.border_thickness + \
            (self.text_size * 0.1), self.y + self.border_thickness + \
            ((self.font_height - self.text_size) / 2)
        self.cursor_x, self.cursor_y = self.cursor_off_x, self.cursor_off_y
        self.cursor_ln = 0
        self.cursor_col = 0

        TextField.textField_list.append(self)
        list.append(self)

    def get_string(self) -> str:
        string = ''
        for line in self.content:
            string += line + '\n'
        return string[:len(string) - 1]

    def wrap(self):
        if self.renders[self.cursor_ln].get_width() > self.width - (self.cursor_off_x - self.x) - self.border_thickness and self.content[self.cursor_ln].rfind(' ') != -1:
            wrapped_ln = self.cursor_ln
            self.content.insert(
                self.cursor_ln + 1, self.content[self.cursor_ln][self.content[self.cursor_ln].rfind(' ') + 1:])
            if self.cursor_col >= self.content[self.cursor_ln].rfind(' ') + 1:
                self.cursor_ln += 1
                self.cursor_y = self.cursor_ln * self.text_size + self.cursor_off_y
                self.cursor_col -= len(
                    self.content[wrapped_ln][:self.content[wrapped_ln].rfind(' ') + 1:])
                self.cursor_x = self.font.render(self.content[self.cursor_ln][0:self.cursor_col], 0, (
                    0, 0, 0), (0, 0, 0)).get_width() + self.cursor_off_x
            self.content[wrapped_ln] = self.content[wrapped_ln][:self.content[wrapped_ln].rfind(
                ' ') + 1:]

    def draw(self):
        if self.title != '':
            win.blit(self.title_render, (self.title_x, self.title_y))

        if self.selected:
            self.box.draw(win, self.color, self.selected_color)
        else:
            self.box.draw(win, self.color, self.unselected_color)

        line_num = 0
        self.renders = []
        for line in self.content:
            font_render = self.font.render(line, 1, self.font_color)
            self.renders.append(font_render)
            win.blit(font_render, (self.x + self.border_thickness + (self.text_size * 0.1), self.y + self.border_thickness +
                     (self.text_size * line_num)), pg.Rect(0, 0, self.width - (self.cursor_off_x - self.x) - self.border_thickness, self.font_height))
            line_num += 1
        self.wrap()

        if self.selected:
            pg.draw.line(win, self.cursor_color, (self.cursor_x, self.cursor_y),
                         (self.cursor_x, self.cursor_y + self.text_size))

    def handleInput(event):
        # click detection
        mouse_pos = pg.mouse.get_pos()
        for t in TextField.textField_list:
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                if pg.Rect(t.box.x, t.box.y, t.box.width, t.box.height).collidepoint(mouse_pos):
                    if not t.selected:
                        t.selected = True
                        t.cursor_x = t.renders[len(
                            t.content) - 1].get_width() + t.x + t.border_thickness + (t.text_size * 0.1)
                        t.cursor_y = t.y + t.border_thickness + \
                            (t.text_size * (len(t.content) - 1)) + \
                            ((t.font_height - t.text_size) / 2)
                        t.cursor_ln = len(t.content) - 1
                        t.cursor_col = len(t.content[len(t.content) - 1])
                    else:
                        t.selected = False
                else:
                    t.selected = False

            if event.type == pg.KEYDOWN and t.selected:
                # cursor movement
                if event.key == pg.K_LEFT:
                    t.cursor_col -= 1
                    if t.cursor_col < 0:
                        t.cursor_ln = max([0, t.cursor_ln - 1])
                        t.cursor_col = len(t.content[t.cursor_ln])
                        t.cursor_x, t.cursor_y = t.renders[t.cursor_ln].get_width(
                        ) + t.cursor_off_x, t.cursor_ln * t.text_size + t.cursor_off_y
                    else:
                        t.cursor_x = t.font.render(
                            t.content[t.cursor_ln][0:t.cursor_col], 0, (0, 0, 0), (0, 0, 0)).get_width() + t.cursor_off_x

                if event.key == pg.K_RIGHT:
                    t.cursor_col += 1
                    if t.cursor_col > len(t.content[t.cursor_ln]):
                        t.cursor_ln = min(
                            [len(t.content) - 1, t.cursor_ln + 1])
                        t.cursor_col = 0
                        t.cursor_x, t.cursor_y = t.cursor_off_x, t.cursor_ln * t.text_size + t.cursor_off_y
                    else:
                        t.cursor_x = t.font.render(
                            t.content[t.cursor_ln][0:t.cursor_col], 0, (0, 0, 0), (0, 0, 0)).get_width() + t.cursor_off_x

                # text input
                if event.key == pg.K_BACKSPACE:
                    if (t.cursor_ln, t.cursor_col) != (0, 0):
                        if t.cursor_col != 0:
                            t.content[t.cursor_ln] = t.content[t.cursor_ln][0:t.cursor_col - 1:] + \
                                t.content[t.cursor_ln][t.cursor_col::]
                        t.cursor_col -= 1
                        if t.cursor_col < 0:
                            t.cursor_ln = max([0, t.cursor_ln - 1])
                            t.cursor_col = len(t.content[t.cursor_ln])
                            t.cursor_x, t.cursor_y = t.renders[t.cursor_ln].get_width(
                            ) + t.cursor_off_x, t.cursor_ln * t.text_size + t.cursor_off_y
                            t.content[t.cursor_ln] += t.content[t.cursor_ln + 1]
                            t.content[t.cursor_ln + 1] = ''
                            del (t.content[t.cursor_ln + 1])
                        else:
                            t.cursor_x = t.font.render(
                                t.content[t.cursor_ln][0:t.cursor_col], 0, (0, 0, 0), (0, 0, 0)).get_width() + t.cursor_off_x
                elif event.key == pg.K_RETURN:
                    t.content.insert(t.cursor_ln + 1,
                                     t.content[t.cursor_ln][t.cursor_col::])
                    t.content[t.cursor_ln] = t.content[t.cursor_ln][0:t.cursor_col:]
                    t.cursor_ln += 1
                    t.cursor_col = 0
                    t.cursor_x, t.cursor_y = t.cursor_off_x, t.cursor_ln * t.text_size + t.cursor_off_y
                else:
                    new = t.content[t.cursor_ln][:t.cursor_col] + \
                        event.unicode + t.content[t.cursor_ln][t.cursor_col:]
                    if new != t.content[t.cursor_ln]:
                        t.content[t.cursor_ln] = new
                        t.cursor_col += 1
                        t.cursor_x = t.font.render(
                            t.content[t.cursor_ln][0:t.cursor_col], 0, (0, 0, 0), (0, 0, 0)).get_width() + t.cursor_off_x

    def update():
        for t in TextField.textField_list:

            t.box.height = max(
                [t.height, t.border_thickness + t.text_size * (0.2 + len(t.content))])

            if t.title != '':
                t.title_y = t.y - (t.title_size * 1.1)
                t.title_render = t.title_font.render(
                    t.title, 1, t.title_color)

            t.box.y = t.y

            t.cursor_off_y = t.y + t.border_thickness + \
                ((t.font_height - t.text_size) / 2)
            t.cursor_y = t.cursor_ln * t.text_size + t.cursor_off_y
