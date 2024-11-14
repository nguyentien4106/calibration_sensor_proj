import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports

def init_settings_tab(self):
    self.left_frame = ttk.Frame(self.settings_tab)
    self.right_frame = ttk.Frame(self.settings_tab)
    self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
    self.right_frame.pack(side=tk.LEFT, padx=10, pady=10)

    # Left Column - Port and Baud Rate selection
    ttk.Label(self.left_frame, text="Select COM Port:").pack(pady=5)
    self.port_list = ttk.Combobox(self.left_frame, width=30, state="readonly")
    self.refresh_ports()
    self.port_list.pack(pady=5)

    ttk.Label(self.left_frame, text="Select Baud Rate:").pack(pady=5)
    self.baud_rate = tk.StringVar(value="9600")
    self.baud_rate_entry = ttk.Entry(self.left_frame, textvariable=self.baud_rate, width=30)
    self.baud_rate_entry.pack(pady=5)

    # Right Column - Connect and Disconnect Buttons
    self.connect_button = ttk.Button(self.right_frame, text="Connect", command=self.connect_port)
    self.connect_button.pack(pady=5)

    self.disconnect_button = ttk.Button(self.right_frame, text="Disconnect", command=self.disconnect_port, state=tk.DISABLED)
    self.disconnect_button.pack(pady=5)

    self.refresh_button = ttk.Button(self.right_frame, text="Refresh Ports", command=self.refresh_ports)
    self.refresh_button.pack(pady=5)