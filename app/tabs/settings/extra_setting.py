import tkinter as tk
from tkinter import ttk, messagebox
from constant.options import *
from helpers.common import create_request
from constant.requests import *
import json

SELF_CONFIG = "SELF CONFIG"

def init_extra_settings(self):
    self.grid = tk.Grid()
    # Frame for extra controls
    self.extra_frame = ttk.Frame(self.settings_tab)
    self.extra_frame.pack(pady=10)

    # Dropdown (example options)
    ttk.Label(self.extra_frame, text="LED Mode:").pack(side=tk.LEFT, padx=5)
    self.led_mode_var = tk.StringVar()
    self.led_mode_var.trace_add("write", lambda idx, val, opt: on_led_mode_change(self, idx, val, opt))
    self.led_mode = ttk.Combobox(self.extra_frame, textvariable=self.led_mode_var, width=15, state="readonly")
    self.led_mode['values'] = LED_MODE_SELECTION
    self.led_mode.pack(side=tk.LEFT, padx=5)

    # time to on field
    ttk.Label(self.extra_frame, text="Time On (ms):").pack(side=tk.LEFT, padx=5)
    self.time_on = ttk.Entry(self.extra_frame, width=15)
    self.time_on.pack(side=tk.LEFT, padx=5)

    # time to off field
    self.color_on_var = tk.StringVar()
    ttk.Label(self.extra_frame, text="Color On:").pack(side=tk.LEFT, padx=5)
    self.color_on = ttk.Combobox(self.extra_frame, textvariable=self.color_on_var, width=15, state="readonly")
    self.color_on['values'] = COLOR_ON_OPTIONS
    self.color_on.pack(side=tk.LEFT, padx=5)

    # time to off field
    self.color_off_var = tk.StringVar()
    ttk.Label(self.extra_frame, text="Color On:").pack(side=tk.LEFT, padx=5)
    self.color_off = ttk.Combobox(self.extra_frame, textvariable=self.color_off_var, width=15, state="readonly")
    self.color_off['values'] = COLOR_OFF_OPTIONS
    self.color_off.pack(side=tk.LEFT, padx=5)

    # Update button
    self.update_button = ttk.Button(self.extra_frame, text="Update", command=lambda: update_action(self))
    self.update_button.pack(side=tk.LEFT, padx=5)

    self.extra_controls_shown = True

def update_action(self):
    """Perform an action when the Update button is clicked."""
    led_mode_val = self.led_mode_var.get()
    time_on_val = self.time_on.get()
    color_on_val = self.color_on_var.get()
    color_off_val = self.color_off_var.get()

    if( not led_mode_val or not time_on_val or not color_off_val or not color_off_val):
        messagebox.showerror("Error", "Please input all the required fields!")
        return

    time_on_val = int(time_on_val) if time_on_val.isdecimal() else None

    if(not time_on_val):
        messagebox.showerror("Error", "Time on must be a number.")
        return

    if(color_on_val == color_off_val):
        messagebox.showerror("Error", "Color On must different with Color Off.")
        return
    
    led_mode_data = {
        "mode": led_mode_val
    }

    if led_mode_val == SELF_CONFIG:
        if len(self.leds_ordering) != 20:
            messagebox.showerror("Error", "Finish select the orders.")
            return
        else:
            led_mode_data["ordering"] = self.leds_ordering

    body = create_request(SETUP, {
        "time_on": time_on_val,
        "color_on": color_on_val,
        "color_off": color_off_val,
        "led_mode": led_mode_data
    })
    self.request(body)

    messagebox.showinfo("Update Action", body.decode())

def on_led_mode_change(self, idx, val, opt):
    selected_mode = self.led_mode_var.get()

    if( selected_mode == SELF_CONFIG):
        self.leds_frame = ttk.Frame(self.settings_tab)
        self.leds_frame.pack(padx=10, pady=10, side=tk.LEFT)
        # Create a frame to hold the buttons
        self.ordering_label = ttk.Label(self.settings_tab, text="Ordering: ")
        self.ordering_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.preview_ordering = ttk.Label(self.settings_tab, text="", background='#fff', foreground='#f00')
        self.preview_ordering.pack(side=tk.LEFT, padx=10, pady=10)

        for i in range(1, 21):
            button = tk.Button(self.leds_frame, text=str(i), command=lambda i=i: button_click(self, i))
            self.leds_button.append(button)
            button.grid(row=(i-1)//5, column=(i-1)%5, padx=5, pady=5)  # Arrange in a grid of 5 columns
    else:
        self.leds_frame.pack_forget()
        self.preview_ordering.pack_forget()
        self.ordering_label.pack_forget()

def button_click(self, val):
    self.leds_button[val - 1]["state"] = "disabled"
    self.leds_ordering.append(val)
    self.preview_ordering["text"] = '->'.join(str(x) for x in self.leds_ordering)