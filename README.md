# FRC Scouting Template
---
This repository serves as a template for making data input fields for scouting in FRC competitions. It is scripted using python and uses the pygame GUI module.

## Settings
In the main function, there is an area of code for customizable settings. Most are self explanetory or are explained in the code. It can be found here:


`[...]
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

    applySettings()
[...]`

## Fields
Every field has attributes that can be changed either at initialization or after it. Thiswill list every attribute built to be modified. If there is an "=" after an attribute, it has a default value (eg. "square(width = 4)" will have an optional parameter width, and if not provided will default to 4)