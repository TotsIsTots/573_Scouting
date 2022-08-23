# FRC Scouting Template
---
This repository serves as a template for making data input fields for scouting in FRC competitions. It is scripted using python and uses the pygame GUI module.

## Installation and Running
Python is required for running. If it is not already installed, you can download and install it from [here](https://www.python.org/downloads/). When installing, make sure to select "Add Python 3.xx to PATH" when prompted.
Running this requires the modules pygame, qrcode, and Image to be installed. You can install them with this command, from your command line:
`pip install pygame qrcode Image`

When these modules are installed, clone this repository and run "main.py". Every time a QR Code is generated, it will be saved to the "QR Codes" folder with the date, match number, and team number selected.

## Settings
In the main function, there is an area of code for customizable settings. Most are self explanatory or are explained in the code, here:
```
[...]
    # customize settings
    Scrolling.scroll_speed = 10
    Scrolling.display_height = 600  # scrollable height
    screen_w, screen_h = 800, 450  # initial window dimensions
    window_caption = "FRC Scouting"
    window_icon_path = os.path.join('Assets', 'FRCLogo.png')
    background_path = os.path.join('Assets', 'background.png')
    action_buttons_pos = 350, 350  # position of "Generate" and "Reset" buttons
    action_buttons_size = 50  # size of "Generate" and "Reset" buttons
    generate_button_color = (0, 255, 0)
    generate_text_color = (255, 255, 255)
    reset_button_color = (255, 0, 0)
    reset_text_color = (255, 255, 255)
[...]
```
## Fields
Every input field has values that can be changed at and/or after initialization. They are listed here with their variable types. if there is an "=" after a value, it is optional and a default value is listed. Obviously, a value defined at initialization is already defined for after initialization. Each has methods, all include an update(), draw(self), and handleInput() methods which are already handled in the code and will not be listed here. The TextField object has a special method listed below.

### Header
**At initialization:**
- y: float
- title: str
- size: int
- thickness: float = 2
- color: tuple = (100, 100, 100)
- bold: bool = True

**After Initialization:**
- y: float
- title: str
- size: int
- thickness: float = 2
- color: tuple = (100, 100, 100)
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', size (from init), bold (from init))

### Counter
**At initialization:**
- x: float
- y: float
- size: int
- value: int = 0
- title: str = ""
- title_size: int = 14

**After Initialization:**
- x: float
- y: float
- value: int = 0
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', title_size)
- title_font_color: tuple = (16, 16, 16)
- font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', size)
- font_color: tuple = (0, 0, 0) 

### Dropdown
**At initialization:**
- x: float
- y: float
- width: float
- height: float
- options: list (of strings)
- title: str = ""
- title_size: int = 14

**After initialization:**
- x: float
- y: float
- width: float
- height: float
- options: list (of str)
- selected_num = -1
- opened: bool = 0
- border_thickness: float = 4
- inner_border_thickness: float = 2
- border_color: tuple = (0, 0, 0)
- background_color: tuple = (255, 255, 255)
- font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', height - (border_thickness * 2))
- font_color: tuple = (0, 0, 0)
- title: str = ""
- title_color: tuple = (0, 0, 0)
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', title_size)

### Checkmark
**At initialization:**
- x: float
- y: float
- title: str
- size: int
- check_placement: str = 'l' (u, d, l, and r are accepted)

**After initialization:**
- y: float
- title: str
- title_color: tuple = (0, 0, 0)
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', size)
- box_thickness: float = 4
- box_color: tuple = (255, 255, 255)
- box_border_color: tuple = (0, 0, 0)
- value: bool = False

### TextField
**At initialization:**
- x: float
- y: float
- width: float
- height: float
- text_size: int
- border_thickness: float = 4
- title: str = ''
- title_size: str = 14

**After initialization:**
- y: float
- height: float
- title: str = ''
- title_color: tuple = (0, 0, 0)
- title_font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', title_size)
- font_color: tuple = (0, 0, 0)
- font: [pygame.font.SysFont](https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont) = pg.font.SysFont('arial', text_size)
- content: list (of str) = ['']
- color: tuple = (255, 255, 255)
- unselected_color: tuple = (128, 128, 128)
- selected_color: tuple = (0, 0, 0)
- selected: bool = False
- cursor_color: tuple = (0, 0, 0)

**Methods:**
> get_string(self) -> str

When called on a TextField object, it will return a single string of the compiled content in the object with "\n" used for new lines. 

## Field Initialization
Examples of initialization can be found in the main function.
```
# Initialize data input objects and headers here, QR code lists data in order of initialization
    header_example = UI_Elements.Header(32, 'Game time!', 24)

    dropdown_example = UI_Elements.Dropdown(
        20, 300, 256, 64, ["1", "two", "0011", "IV", "0x05"], "Number", 32)

    check_example = UI_Elements.Checkmark(350, 50, "Water game?", 64)

    text_field_example = UI_Elements.TextField(
        350, 180, 256, 128, 24, title='Notes', title_size=24)
```
Indents under examples are just formatting and are not required, it can all be on one line.
