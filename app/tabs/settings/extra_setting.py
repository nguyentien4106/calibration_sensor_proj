import tkinter as tk
from tkinter import ttk, messagebox
from constant.options import *
from helpers.common import create_request

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
    
    self.request(
        create_request(SETUP, {
            "time_on": time_on_val,
            "color_on": color_on_val,
            "color_off": color_off_val,
            "led_mode": {
                "mode": led_mode_val
            }
        })
    )
    messagebox.showinfo("Update Action", f"led_mode_val: {led_mode_val}, time_on_val: {time_on_val}, color_on_val: {color_on_val},color_off_val {color_off_val} ")

def on_led_mode_change(self, idx, val, opt):
    selected_mode = self.led_mode_var.get()
    self.leds_frame = tk.Frame(self.settings_tab)

    if( selected_mode == "SELF CONFIG"):
        self.leds_frame.pack(padx=10, pady=10, side=tk.LEFT)
        # Create a frame to hold the buttons
        ttk.Label(self.settings_tab, text="Ordering: ").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.preview_ordering = ttk.Label(self.settings_tab, text="", background='#fff', foreground='#f00')
        self.preview_ordering.pack(side=tk.LEFT, padx=10, pady=10)

        for i in range(1, 21):
            button = tk.Button(self.leds_frame, text=str(i), command=lambda i=i: button_click(self, i))
            self.leds_button.append(button)
            button.grid(row=(i-1)//5, column=(i-1)%5, padx=5, pady=5)  # Arrange in a grid of 5 columns
    else:
        print('destroy', self.leds_frame)
        self.leds_frame.destroy()
        self.leds_frame = None

def button_click(self, val):
    self.leds_button[val - 1]["state"] = "disabled"
    self.leds_ordering.append(val)
    self.preview_ordering["text"] = '->'.join(str(x) for x in self.leds_ordering)