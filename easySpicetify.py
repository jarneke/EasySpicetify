# Place your spicetify root folder in between the "" down below
# (example: "C:\Users\Jhon\spicetify-themes")
# ----------------
your_root_folder = r"C:\Users\Jarne\spicetify-themes"
# ----------------
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


def apply_colors():
    for item, color in colors.items():
        command = f"spicetify color {item} {color}"
        os.system(command)
    os.system("spicetify apply")


def get_current_colors():
    command = "spicetify color"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    lines = result.stdout.split("\n")
    for line in lines:
        line = re.sub(r"\x1b\[[0-9;]*m", "", line)
        parts = line.split("|")
        if len(parts) >= 3:
            item = parts[0].strip().split()[0]
            hex_color = "#" + parts[1].strip()
            if item in buttons:
                colors[item] = hex_color
                buttons[item].config(style=f"{item}.TButton")
                color_labels[item].config(
                    text=hex_color,
                    bg=hex_color,
                    fg="white" if not is_bright(hex_color) else "black",
                )


def get_items():
    items = []
    command = "spicetify color"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    lines = result.stdout.split("\n")
    for line in lines:
        line = re.sub(r"\x1b\[[0-9;]*m", "", line)
        parts = line.split("|")
        if len(parts) >= 3:
            item = parts[0].strip().split()[0]
            items.append(item)
    return items


def is_bright(color):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness > 127


def get_theme_folders(root_folder):
    theme_folders = []

    for item in os.listdir(root_folder):
        item_path = os.path.join(root_folder, item)
        if (
            os.path.isdir(item_path)
            and "color.ini" in os.listdir(item_path)
            and "user.css" in os.listdir(item_path)
        ):
            theme_folders.append(item)

    return theme_folders


def get_current_theme():
    command = "spicetify config current_theme"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    current_theme = result.stdout.strip()

    return current_theme


# Function to apply the theme and color scheme
def apply_theme(theme_name, color_scheme):
    command = f"spicetify config current_theme {theme_name} color_scheme {color_scheme} && spicetify apply"
    subprocess.run(command, shell=True)


def get_schemes(root_folder):
    theme = get_current_theme()
    color_file_path = os.path.join(root_folder, theme, "color.ini")
    if not os.path.exists(color_file_path):
        print(f"No color.ini found for theme {theme}")
        return {}

    color_file = cp.ConfigParser()
    color_file.read(color_file_path)

    scheme_dict = {}
    for section in color_file.sections():
        scheme_dict[section] = dict(color_file[section])

    return scheme_dict


def select_theme(theme):
    command = f"spicetify config current_theme {theme}"
    os.system(command)
    os.system("spicetify apply")


items = get_items()
colors = {}
buttons = {}
color_labels = {}
root_folder = your_root_folder
theme_list = get_theme_folders(root_folder)
current_theme = get_current_theme()
scheme_dict = get_schemes(root_folder)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        self.configure(bg="black")
        self.title("Main Window")
        self.iconbitmap("assets/icons/candle_icon_257233.ico")

        style = ttk.Style()
        style.configure("TButton", background="black")

        welcome_label = tk.Label(
            self, text="Welcome to Easy Spicetify!", bg="black", fg="white", pady=10
        )
        welcome_label.pack()

        instruction_label = tk.Label(
            self,
            text="Please choose between config and color.",
            bg="black",
            fg="white",
            pady=10,
        )
        instruction_label.pack()

        ttk.Button(
            self,
            text="Open Color Window",
            command=self.open_color_window,
            style="TButton",
        ).pack()
        ttk.Button(
            self,
            text="Open Config Window",
            command=self.open_config_window,
            style="TButton",
        ).pack()

    def open_color_window(self):
        self.color_window = ColorWindow(self)

    def open_config_window(self):
        self.config_window = ConfigWindow(self)


class ColorWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(bg="black")
        self.title("Color Window")
        self.iconbitmap("assets/icons/candle_icon_257233.ico")

        style = ttk.Style()
        style.configure("TButton", background="black")

        rows = 9
        cols = 4

        for i, item in enumerate(items):
            row = i // cols
            col = i % cols

            style.configure(f"{item}.TButton", background="black")

            button = ttk.Button(
                self,
                text=f"Select Color for {item}",
                command=lambda item=item: select_color(item),
                style=f"{item}.TButton",
            )
            button.grid(row=row, column=col, sticky="ew")
            buttons[item] = button

        for i, item in enumerate(items):
            row = (i // cols) + rows
            col = i % cols

            label = tk.Label(self, text="", bg="black")
            label.grid(row=row, column=col, sticky="ew")
            color_labels[item] = label

        apply_button = ttk.Button(
            self, text="Apply Colors", command=apply_colors, style="TButton"
        )
        apply_button.grid(
            row=row + 1, column=0, columnspan=cols, sticky="ew", padx=5, pady=5
        )
        get_colors_button = ttk.Button(
            self,
            text="Get current color scheme",
            command=get_current_colors,
            style="TButton",
        )
        get_colors_button.grid(
            row=row + 2, column=0, columnspan=cols, sticky="ew", padx=5, pady=5
        )

    def go_back(self):
        self.master.deiconify()
        self.destroy()

    def protocol(self, name, func):
        if name == "WM_DELETE_WINDOW":
            self.master.deiconify()
        super().protocol(name, func)


class ConfigWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # gui code
        self.geometry("400x350")
        self.configure(bg="black")
        self.title("config Window")
        self.iconbitmap("assets/icons/candle_icon_257233.ico")

        style = ttk.Style()
        style.configure("TButton", background="black")

        welcome_label = tk.Label(
            self, text="Welcome to config menu!", bg="black", fg="white", pady=10
        )
        welcome_label.pack()

        instruction_label = tk.Label(
            self,
            text="Please choose between current theme and color scheme.",
            bg="black",
            fg="white",
            pady=10,
            padx=5,
        )
        instruction_label.pack()

        config_info_label = tk.Label(
            self,
            text='Current theme window is used to change the theme of spicetify,\n to find wich theme you like you can take a look here: \n\n"https://github.com/spicetify/spicetify-themes"\n',
            bg="black",
            fg="white",
            pady=5,
        )
        config_info_label.pack()

        scheme_info_label = tk.Label(
            self,
            text='Color scheme window is used to change the color scheme of the theme\n you can also find these color schemes at: \n\n"https://github.com/spicetify/spicetify-themes"\n',
            bg="black",
            fg="white",
            pady=5,
        )
        scheme_info_label.pack()

        ttk.Button(
            self,
            text="Open current theme window",
            command=self.open_theme_window,
            style="TButton",
        ).pack()

        ttk.Button(
            self,
            text="Open color scheme Window",
            command=self.open_scheme_window,
            style="TButton",
        ).pack()

    def go_back(self):
        self.master.deiconify()
        self.destroy()

    def open_theme_window(self):
        self.ThemeWindow = ThemeWindow(self)

    def open_scheme_window(self):
        self.SchemeWindow = SchemeWindow(self)


class SchemeWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        theme = get_current_theme()
        scheme_dict = get_schemes(root_folder)
        # gui code
        self.geometry("400x200")
        self.configure(bg="black")
        self.title("color scheme Window")
        self.iconbitmap("assets/icons/candle_icon_257233.ico")

        style = ttk.Style()
        style.configure("TButton", background="black")

        # Create a variable to hold the selected color scheme
        selected_scheme = tk.StringVar(self)

        # Check if scheme_dict is empty and set a default value accordingly
        if scheme_dict:
            selected_scheme.set(next(iter(scheme_dict)))
        else:
            selected_scheme.set("DefaultScheme")  # Adjust this default value as needed

        # Create a dropdown menu (OptionMenu) for the color schemes
        ttk.OptionMenu(self, selected_scheme, *scheme_dict.keys()).pack()

        # Create a button that will apply the selected color scheme when clicked
        ttk.Button(
            self,
            text="Apply",
            command=lambda: apply_theme(theme, selected_scheme.get()),
        ).pack()

    def go_back(self):
        self.master.deiconify()
        self.destroy()


class ThemeWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # gui code
        self.configure(bg="black")
        self.title("cuurent theme Window")
        self.iconbitmap("assets/icons/candle_icon_257233.ico")

        style = ttk.Style()
        style.configure("TButton", background="black")

        cols = 4

        for t, theme in enumerate(theme_list):
            row = t // cols
            col = t % cols

            style.configure(f"{theme}.TButton", background="black")

            button = ttk.Button(
                self,
                text=f"use {theme} theme",
                command=lambda theme=theme: select_theme(theme),
                style=f"{theme}.TButton",
            )
            button.grid(row=row, column=col, sticky="ew")
            buttons[theme] = button

    def go_back(self):
        self.master.deiconify()
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
