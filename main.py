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
    for c in UI_Elements.Counter.counter_list:
        # pg.draw.rect(WIN, ORANGE, pg.Rect(c.x, c.y, c.width, c.height)) #draw dimensions
        # UI_Elements.borderRect(c.x, c.y, c.width, c.height, 5).draw(
        #     WIN, (255, 255, 255), (0, 0, 0))
        c.draw()

    for d in UI_Elements.Dropdown.dropdown_list:
        # pg.draw.rect(WIN, ORANGE, pg.Rect(c.x, c.y, c.width, c.height)) #draw dimensions
        # UI_Elements.borderRect(c.x, c.y, c.width, c.height, 5).draw(
        #     WIN, (255, 255, 255), (0, 0, 0))
        d.draw()

    for c in UI_Elements.Checkmark.checkmark_list:
        c.draw()

    pg.display.update()


def main():
    # define data input parameters here
    counter_test = UI_Elements.Counter(20, 72, 64, 0, "High Goal", 32)
    dropdown_test = UI_Elements.Dropdown(
        20, 208, 256, 64, ["1", "two", "0011", "IV", "0x05"], "number", 32)
    check_test = UI_Elements.Checkmark(400, 20, "yes?", 64,)
    check_test.title_color = (255, 0, 0)
    check_test.box_thickness = 2

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                UI_Elements.Counter.handleInput()
                UI_Elements.Dropdown.handleInput()
                UI_Elements.Checkmark.handleInput()

        screen_w, screen_h = pg.display.get_surface().get_size()

        UI_Elements.Counter.update()
        UI_Elements.Dropdown.update()
        UI_Elements.Checkmark.update()

        drawDisplay(screen_w, screen_h)


if __name__ == '__main__':
    main()
