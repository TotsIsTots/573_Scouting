import qrcode
import pygame as pg
import os

pg.font.init()


def saveAndShow(name: str, data: str, size: float, original_display_size: tuple):
    display = pg.display.set_mode((size, size))

    img = qrcode.make(data)
    img.save(os.path.join('QR Codes', name + '.png'))
    img = pg.transform.scale(pg.image.load(
        os.path.join('QR Codes', name + '.png')), (size, size))

    arial = pg.font.SysFont('arial', size // 16)

    showing = True
    while showing:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                showing = False

            if event.type == pg.QUIT:
                showing = False

        display.blit(img, (0, 0))
        display.blit(arial.render('Click to continue', 1,
                     (0, 0, 0), (255, 255, 255)), (size // 64, 0))
        pg.display.flip()

    pg.display.set_mode(original_display_size, pg.RESIZABLE)
