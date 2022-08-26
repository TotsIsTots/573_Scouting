import Scrolling
import UI_Elements
import QR
import pygame as pg
import math
from datetime import date
import configparser


def main():
    # it is HIGHLY reccomended that these exist, but you can change parameters such as size, position etc.
    global match_number, team_number
    match_number = UI_Elements.Counter(
        20, 80, 64, 1, "Match number", 32)
    team_number = UI_Elements.TextField(
        20, 200, 128, 32, 30, title='Team Number', title_size=32)

    # Initialize data input objects and headers here, QR code lists data in order of initialization
    header_example = UI_Elements.Header(32, 'Game time!', 24)

    dropdown_example = UI_Elements.Dropdown(
        20, 300, 256, 64, ["1", "two", "0011", "IV", "0x05"], "Number", 32)

    check_example = UI_Elements.Checkmark(350, 50, "Water game?", 64)

    text_field_example = UI_Elements.TextField(
        350, 180, 256, 128, 24, title='Notes', title_size=24)

    # All code below this line is for drawing the display, handling inputs, generating QR codes, etc.
    # It is not reccomended to change anything below this line.

    # main loop
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # handles input for UI elements
            UI_Elements.TextField.handleInput(event)
            UI_Elements.Dropdown.handleInput(event)
            UI_Elements.Checkmark.handleInput(event)
            UI_Elements.Counter.handleInput(event)

            # Generate and Reset buttons
            handleActionInputs(event)

            # handles scrolling from scroll offset
            handleScrolling(Scrolling.get_change(event))

        screen_w, screen_h = pg.display.get_surface().get_size()

        # updates UI elements
        UI_Elements.Header.update()
        UI_Elements.Counter.update()
        UI_Elements.Dropdown.update()
        UI_Elements.Checkmark.update()
        UI_Elements.TextField.update()

        drawDisplay(screen_w, screen_h)


pg.font.init()

WIN = pg.display.set_mode((800, 450))

# initialize other scripts
Scrolling.init()
UI_Elements.init()

# load settings from config file
config = configparser.ConfigParser()
config.read('config.ini')

Scrolling.scroll_speed = int(config['Scrolling']['scroll_speed'])
Scrolling.display_height = int(config['Scrolling']['display_height'])

screen_w = int(config['Window']['screen_w'])
screen_h = int(config['Window']['screen_h'])
window_caption = config['Window']['window_caption']
window_icon_path = config['Window']['window_icon_path']
background_path = config['Window']['background_path']

action_buttons_pos = tuple(
    map(int, config['ActionButtons']['action_buttons_pos'].split(',')))
action_buttons_size = int(config['ActionButtons']['action_buttons_size'])
generate_button_color = tuple(
    map(int, config['ActionButtons']['generate_button_color'].split(',')))
generate_text_color = tuple(
    map(int, config['ActionButtons']['generate_text_color'].split(',')))
reset_button_color = tuple(
    map(int, config['ActionButtons']['reset_button_color'].split(',')))
reset_text_color = tuple(
    map(int, config['ActionButtons']['reset_text_color'].split(',')))

QR_display_size = int(config['QRCodes']['display_size'])
QR_save_path = config['QRCodes']['save_path']

WIN = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)
pg.display.set_caption(window_caption)
icon = pg.image.load(window_icon_path)
pg.display.set_icon(icon)
BACKGROUND = pg.image.load(background_path)
BACKGROUND_W, BACKGROUND_H = BACKGROUND.get_size()

action_font = pg.font.SysFont('arial', action_buttons_size)
generate_render = action_font.render('Generate', 1, generate_text_color)
generate_rect = pg.Rect(
    action_buttons_pos[0], action_buttons_pos[1], generate_render.get_width() * 1.1, action_buttons_size)
reset_render = action_font.render('Reset', 1, reset_text_color)
reset_rect = pg.Rect(
    action_buttons_pos[0] + generate_render.get_width() * 1.2, action_buttons_pos[1], reset_render.get_width() * 1.1, action_buttons_size)


def compileData(seperator: str = ';') -> str:
    data = ''
    for element in UI_Elements.list:
        if type(element).__name__ == "Counter" or type(element).__name__ == "Checkmark":
            data += str(element.value) + seperator
        if type(element).__name__ == "Dropdown":
            data += element.selected_str + seperator
        if type(element).__name__ == "TextField":
            data += element.get_string() + seperator
    return data[:len(data) - len(seperator)]


def reset():
    for element in UI_Elements.list:
        if type(element).__name__ == "Counter":
            if element != match_number:
                element.value = 0
        if type(element).__name__ == "Checkmark":
            element.value = False
        if type(element).__name__ == "Dropdown":
            element.selected_num = -1
        if type(element).__name__ == "TextField":
            element.content = ['']


def handleScrolling(scroll_change):
    for header in UI_Elements.Header.header_list:
        header.y -= scroll_change
    for counter in UI_Elements.Counter.counter_list:
        counter.y -= scroll_change
    for checkmark in UI_Elements.Checkmark.checkmark_list:
        checkmark.y -= scroll_change
    for dropdown in UI_Elements.Dropdown.dropdown_list:
        dropdown.y -= scroll_change
    for textField in UI_Elements.TextField.textField_list:
        textField.y -= scroll_change

    generate_rect.y -= scroll_change
    reset_rect.y -= scroll_change


def handleActionInputs(event):
    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
        mouse_pos = pg.mouse.get_pos()
        if generate_rect.collidepoint(mouse_pos):
            QR.saveAndShow(str(date.today()) + '_Match_' + str(match_number.value) +
                           '_Team_' + team_number.content[0], compileData(), QR_display_size, (screen_w, screen_h), QR_save_path)
        if reset_rect.collidepoint(mouse_pos):
            reset()


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
    for header in UI_Elements.Header.header_list:
        header.draw()

    pg.draw.rect(WIN, generate_button_color, generate_rect,
                 border_radius=action_buttons_size // 5)
    WIN.blit(generate_render, (generate_rect.x +
             generate_render.get_width() * .05, generate_rect.y - ((generate_render.get_height() - action_buttons_size) / 2)))
    pg.draw.rect(WIN, reset_button_color, reset_rect,
                 border_radius=action_buttons_size // 5)
    WIN.blit(reset_render, (reset_rect.x +
             reset_render.get_width() * .05, reset_rect.y - ((reset_render.get_height() - action_buttons_size) / 2)))

    Scrolling.drawScrollBar()

    pg.display.flip()


if __name__ == '__main__':
    main()
