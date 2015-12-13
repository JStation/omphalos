from pyglet_gui.theme import Theme

action_menu_theme = Theme(
    {
        "font": "Lucida Grande",
        "font_size": 10,
        "text_color": [255, 255, 255, 255],
        "gui_color": [255, 0, 0, 255],
        "button": {
           "down": {
               "image": {
                   "source": "button-down.png",
                   "frame": [8, 6, 2, 2],
                   "padding": [18, 18, 8, 6]
               },
               "text_color": [0, 0, 0, 255]
           },
           "up": {
               "image": {
                   "source": "button.png",
                   "frame": [6, 5, 6, 3],
                   "padding": [18, 18, 8, 6]
               }
           }
        },
        "vscrollbar": {
           "knob": {
               "image": {
                   "source": "vscrollbar.png",
                   "region": [0, 16, 16, 16],
                   "frame": [0, 6, 16, 4],
                   "padding": [0, 0, 0, 0]
               },
               "offset": [0, 0]
           },
           "bar": {
               "image": {
                   "source": "vscrollbar.png",
                   "region": [0, 64, 16, 16]
               },
               "padding": [0, 0, 0, 0]
           }
        }
    }, resources_path='theme/')

resource_menu_theme = Theme(
    {
        "font": "Lucida Grande",
        "font_size": 8,
        "text_color": [255, 255, 255, 255],
        "gui_color": [255, 0, 0, 255],
        "button": {
           "down": {
               "image": {
                   "source": "button-down.png",
                   "frame": [8, 6, 2, 2],
                   "padding": [18, 18, 8, 6]
               },
               "text_color": [0, 0, 0, 255]
           },
           "up": {
               "image": {
                   "source": "button.png",
                   "frame": [6, 5, 6, 3],
                   "padding": [18, 18, 8, 6]
               }
           }
        },
        "section": {
           "right": {
               "image": {
                   "source": "line.png",
                   "region": [2, 0, 6, 4],
                   "frame": [0, 4, 4, 0],
                   "padding": [0, 0, 0, 6]
               }
           },
           "font_size": 10,
           "opened": {
               "image": {
                   "source": "book-open.png"
               }
           },
           "closed": {
               "image": {
                   "source": "book.png"
               }
           },
           "left": {
               "image": {
                   "source": "line.png",
                   "region": [0, 0, 6, 4],
                   "frame": [2, 4, 4, 0],
                   "padding": [0, 0, 0, 6]
               }
           },
           "center": {
               "image": {
                   "source": "line.png",
                   "region": [2, 0, 4, 4],
                   "frame": [0, 4, 4, 0],
                   "padding": [0, 0, 0, 6]
               }
           }
        },
        "frame": {
           "image": {
               "source": "panel.png",
               "frame": [8, 8, 16, 16],
               "padding": [16, 16, 8, 8]
           }
        }
    }, resources_path='theme/')