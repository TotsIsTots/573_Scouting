import dis
from platform import win32_edition
import pygame as pg
import main

# define the window surface as the one used in main (in this case, 'WIN')


scroll_off = 0
scroll_change = 0
scroll_speed = 1

display_height = 1000


def init():
    global win
    # define the window surface as the one used in main (in this case, 'WIN')
    win = main.WIN


def get_off(event) -> float:
    global scroll_off
    global scroll_speed
    screen_h = pg.display.get_surface().get_size()[1]
    if event.type == pg.MOUSEBUTTONDOWN and screen_h < display_height:
        if event.button == 4:
            scroll_off -= scroll_speed
            if scroll_off < 0:
                scroll_off = 0
        if event.button == 5:
            scroll_off += scroll_speed
            if scroll_off > display_height - screen_h:
                scroll_off = display_height - screen_h
    scroll_off = float(scroll_off)
    return scroll_off


def get_change(event):
    global scroll_change
    global scroll_off
    global scroll_speed
    old_scroll_off = scroll_off
    screen_h = pg.display.get_surface().get_size()[1]
    if event.type == pg.MOUSEBUTTONDOWN and screen_h < display_height:
        if event.button == 4:
            scroll_off -= scroll_speed
            if scroll_off < 0:
                scroll_off = 0
        if event.button == 5:
            scroll_off += scroll_speed
            if scroll_off > display_height - screen_h:
                scroll_off = display_height - screen_h
    scroll_off = float(scroll_off)
    scroll_change = float(scroll_off - old_scroll_off)
    return scroll_change


def drawScrollBar(thickness: float = 8):
    screen_w, screen_h = pg.display.get_surface().get_size()
    bar = pg.Surface((thickness, screen_h))
    bar.fill((150, 150, 150))
    bar.set_alpha(160)
    win.blit(bar, (screen_w - thickness, 0))

    if screen_h < display_height:
        scroller = pg.Surface((thickness, screen_h ** 2 / display_height))
        scroller.fill((100, 100, 100))
        scroller.set_alpha(160)
        win.blit(scroller, (screen_w - thickness,
                 scroll_off * screen_h / display_height))
    else:
        scroller = pg.Surface((thickness, screen_h))
        scroller.fill((100, 100, 100))
        scroller.set_alpha(160)
        win.blit(scroller, (screen_w - thickness, 0))
