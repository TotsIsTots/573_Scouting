import pygame as pg
import os
import math

import UI_Elements

pg.font.init()

screen_w, screen_h = 900, 500  # initial window dimensions
WIN = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)
pg.display.set_caption("FRC Scouting")

WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)


def clear(): return os.system('cls')


ARIAL = pg.font.SysFont('arial', 24)

BACKGROUND = pg.image.load(os.path.join('Assets', 'background.png'))
BACKGROUND_W = BACKGROUND.get_width()
BACKGROUND_H = BACKGROUND.get_height()


def drawBackground(screen_w, screen_h):
    for x in range(math.floor(screen_w / BACKGROUND_W) + 1):
        for y in range(math.floor(screen_h / BACKGROUND_H) + 1):
            WIN.blit(BACKGROUND, (x * BACKGROUND_W, y * BACKGROUND_H))


def drawDisplay(screen_w, screen_h):
    drawBackground(screen_w, screen_h)
    for counter in UI_Elements.Counter.counter_list:
        counter.draw()

    for checkmark in UI_Elements.Checkmark.checkmark_list:
        checkmark.draw()

    for dropdown in UI_Elements.Dropdown.dropdown_list:
        dropdown.draw()

    for textField in UI_Elements.TextField.textField_list:
        textField.draw()

    pg.display.flip()


def main():
    # define data input parameters here
    counter_test = UI_Elements.Counter(20, 72, 64, 0, "High Goal", 32)

    dropdown_test = UI_Elements.Dropdown(
        20, 208, 256, 64, ["1", "two", "0011", "IV", "0x05"], "number", 32)

    check_test = UI_Elements.Checkmark(400, 20, "yes?", 64)
    check_test.title_color = (255, 0, 0)
    check_test.box_thickness = 2

    text_field_test = UI_Elements.TextField(
        400, 128, 256, 128, 24, title='test', title_size=24)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            UI_Elements.TextField.handleInput(event)
            UI_Elements.Dropdown.handleInput(event)
            UI_Elements.Checkmark.handleInput(event)
            UI_Elements.Counter.handleInput(event)

        screen_w, screen_h = pg.display.get_surface().get_size()

        UI_Elements.Counter.update()
        UI_Elements.Dropdown.update()
        UI_Elements.Checkmark.update()
        UI_Elements.TextField.update()

        drawDisplay(screen_w, screen_h)


if __name__ == '__main__':
    main()
