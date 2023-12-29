# Ok so allot of chat-GPT has been used as i had basically no Python knowledge

import tkinter as tk
from tkinter import ttk, colorchooser
import os
import subprocess
import re
import configparser as cp


def select_color(item):
    color_code = colorchooser.askcolor(title=f"Choose color for {item}")
    hex_color = "#%02x%02x%02x" % (
        int(color_code[0][0]),
        int(color_code[0][1]),
        int(color_code[0][2]),
    )
    colors[item] = hex_color
    buttons[item].config(style=f"{item}.TButton")
    color_labels[item].config(
        text=hex_color,
        bg=hex_color,
        fg="white" if not is_bright(hex_color) else "black",
    )
