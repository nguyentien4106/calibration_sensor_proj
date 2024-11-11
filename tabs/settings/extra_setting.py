import tkinter as tk
from tkinter import ttk, messagebox
from constant.options import *

def init_extra_settings(self):
    # Frame for extra controls
    self.extra_frame = ttk.Frame(self.settings_tab)
    self.extra_frame.pack(pady=10)

    # Dropdown (example options)
    ttk.Label(self.extra_frame, text="LED Mode:").pack(side=tk.LEFT, padx=5)
    self.option_var = tk.StringVar()
    self.option_dropdown = ttk.Combobox(self.extra_frame, textvariable=self.option_var, width=15)
    self.option_dropdown['values'] = LED_MODE_SELECTION
    self.option_dropdown.pack(side=tk.LEFT, padx=5)

    # time to on field
    ttk.Label(self.extra_frame, text="Time On (ms):").pack(side=tk.LEFT, padx=5)
    self.time_on = ttk.Entry(self.extra_frame, width=15)
    self.time_on.pack(side=tk.LEFT, padx=5)

    # time to off field
    ttk.Label(self.extra_frame, text="Time Off (ms):").pack(side=tk.LEFT, padx=5)
    self.time_off = ttk.Entry(self.extra_frame, width=15)
    self.time_off.pack(side=tk.LEFT, padx=5)

    # Update button
    self.update_button = ttk.Button(self.extra_frame, text="Update", command=lambda: update_action(self))
    self.update_button.pack(side=tk.LEFT, padx=5)

    self.extra_controls_shown = True

def update_action(self):
    """Perform an action when the Update button is clicked."""
    selected_option = self.option_var.get()
    input_value = self.time_on.get()
    messagebox.showinfo("Update Action", f"Option: {selected_option}, Value: {input_value}")