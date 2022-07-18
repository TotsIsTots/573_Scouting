import pygame as pg
import os
import math

import UI_Elements

pg.font.init()

screen_w, screen_h = 900, 500  # initial window dimensions
WIN = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)
pg.display.set_caption("FRC Scouting")

WHITE = (255, 255, 255)

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
    for c in UI_Elements.counter_list:
        c.draw()
    UI_Elements.counter.update()
    pg.display.update()


def main():
    counter_test = UI_Elements.counter(20, 72, 64, 0, "High Goal", 32)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                for c in UI_Elements.counter_list:
                    if c.minus_rect.collidepoint(mouse_pos):
                        c.value -= 1
                    if c.plus_rect.collidepoint(mouse_pos):
                        c.value += 1

        screen_w, screen_h = pg.display.get_surface().get_size()

        drawDisplay(screen_w, screen_h)


if __name__ == '__main__':
    main()
