import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
from tabs.settings_tab import *

class SerialPortApp:
    def __init__(self, root : tk.Tk):
        self.root = root
        self.root.title("COM Port Tool")

        # Initialize serial port and thread control flag
        self.serial_port = None
        self.stop_thread = False

        # Variables for extra controls
        self.extra_controls_shown = False
        self.option_dropdown = None
        self.extra_input = None

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.settings_tab = ttk.Frame(self.tab_control)
        self.data_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.settings_tab, text="Settings")
        self.tab_control.add(self.data_tab, text="Data")
        self.tab_control.pack(expand=1, fill="both")

        # Setup Settings Tab with column layout
        self.setup_settings_tab()

        # Setup Data Tab
        self.setup_data_tab()

    def setup_settings_tab(self):
        init_settings_tab(self)

    def setup_data_tab(self):
        # Data display area
        self.data_display = tk.Text(self.data_tab, height=15, width=50)
        self.data_display.pack(pady=10)
        self.data_display.insert(tk.END, "Data received from COM port will appear here.\n")

    def refresh_ports(self):
        """Refresh the list of available COM ports."""
        ports = serial.tools.list_ports.comports()
        self.port_list["values"] = [port.device for port in ports]

    def connect_port(self):
        """Connect to the selected COM port and start receiving data in a new thread."""
        port = self.port_list.get()
        baud_rate = self.baud_rate.get()

        if port and baud_rate:
            try:
                threading.Thread(target=self.connect_in_background, args=(port, baud_rate), daemon=True).start()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Could not open port {port}: {e}")
        else:
            messagebox.showwarning("Input Required", "Please select a port and enter a baud rate.")

    def connect_in_background(self, port, baud_rate):
        """Handle COM port connection in a background thread and update UI on success/failure."""
        try:
            self.serial_port = serial.Serial(port, int(baud_rate), timeout=1)
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Connected to {port}"))
            self.root.after(0, self.enable_controls)

            # Show extra controls after successful connection
            self.root.after(0, self.show_extra_controls)

            # Start the background thread for receiving data
            self.stop_thread = False
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.receive_thread.start()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Connection Error", f"Could not open port {port}: {e}"))

    def show_extra_controls(self):
        """Show additional controls in the Settings tab after connecting to a port."""
        if self.extra_controls_shown:
            return  # Avoid adding controls multiple times

        # Frame for extra controls
        self.extra_frame = ttk.Frame(self.settings_tab)
        self.extra_frame.pack(pady=10)

        # Dropdown (example options)
        ttk.Label(self.extra_frame, text="Select Option:").pack(side=tk.LEFT, padx=5)
        self.option_var = tk.StringVar()
        self.option_dropdown = ttk.Combobox(self.extra_frame, textvariable=self.option_var, width=15)
        self.option_dropdown['values'] = ['Option 1', 'Option 2', 'Option 3']
        self.option_dropdown.pack(side=tk.LEFT, padx=5)

        # Input field
        ttk.Label(self.extra_frame, text="Enter Value:").pack(side=tk.LEFT, padx=5)
        self.extra_input = ttk.Entry(self.extra_frame, width=15)
        self.extra_input.pack(side=tk.LEFT, padx=5)

        # Update button
        self.update_button = ttk.Button(self.extra_frame, text="Update", command=self.update_action)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.extra_controls_shown = True

    def update_action(self):
        """Perform an action when the Update button is clicked."""
        selected_option = self.option_var.get()
        input_value = self.extra_input.get()
        messagebox.showinfo("Update Action", f"Option: {selected_option}, Value: {input_value}")

    def send_message(self):
        """Send a message to the connected COM port."""
        if self.serial_port and self.serial_port.is_open:
            message = self.message_entry.get()
            self.serial_port.write(message.encode('utf-8'))
            messagebox.showinfo("Message Sent", f"Sent: {message}")
        else:
            messagebox.showwarning("Not Connected", "Please connect to a COM port first.")

    def receive_data(self):
        """Function to continuously read incoming data in a separate thread."""
        while not self.stop_thread and self.serial_port and self.serial_port.is_open:
            try:
                data = self.serial_port.readline().decode('utf-8').strip()
                if data:
                    self.root.after(0, self.update_display, data)
            except Exception as e:
                self.root.after(0, self.update_display, f"Error reading data: {e}")
            time.sleep(0.1)

    def update_display(self, message):
        """Update the data display in the Data tab."""
        self.data_display.insert(tk.END, f"{message}\n")
        self.data_display.see(tk.END)

    def enable_controls(self):
        """Enable Send and Disconnect buttons after a successful connection."""
        self.send_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.DISABLED)

    def disconnect_port(self):
        """Disconnect from the COM port and stop the receive thread."""
        self.stop_thread = True  # Stop the receive thread

        # Close the serial port if it's open
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            messagebox.showinfo("Disconnected", "COM port disconnected successfully.")

        # Disable Send and Disconnect buttons, enable Connect button
        self.send_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.DISABLED)
        self.connect_button.config(state=tk.NORMAL)

        # Hide the extra controls on disconnection
        self.hide_extra_controls()

    def hide_extra_controls(self):
        """Hide or destroy the extra controls when disconnecting."""
        if self.extra_controls_shown:
            self.extra_frame.pack_forget()
            self.extra_controls_shown = False

    def on_closing(self):
        """Handle app closure by stopping the background thread and closing the serial port."""
        self.stop_thread = True
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        if hasattr(self, 'receive_thread'):
            self.receive_thread.join()  # Wait for the thread to finish
        self.root.destroy()

# Initialize Tkinter and the app
root = tk.Tk()
app = SerialPortApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Properly close on exit
root.mainloop()
