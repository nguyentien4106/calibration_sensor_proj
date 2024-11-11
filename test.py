import serial
import time

# Define the virtual COM ports
send_port = "COM5"  # Change to the name of your first virtual COM port
receive_port = "COM6"  # Change to the name of your second virtual COM port

# Initialize the sender port
sender = serial.Serial(send_port, baudrate=9600, timeout=1)
receiver = serial.Serial(receive_port, baudrate=9600, timeout=1)

# Send data
data_to_send = "Hello from COM5 to COM6!"
print(f"Sending data: {data_to_send}")
sender.write(data_to_send.encode())

# Give some time for data to be transmitted
time.sleep(1)

# Read data from the receiving port
if receiver.in_waiting > 0:
    received_data = receiver.read(receiver.in_waiting).decode()
    print(f"Received data: {received_data}")
else:
    print("No data received.")

# Close ports
sender.close()
receiver.close()