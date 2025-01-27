import serial
import time

def communicate_with_meter(port):
    """
    Communicates with the Landis+Gyr E230 meter via the given serial port.
    
    Args:
        port (str): Path to the serial port (e.g., '/dev/ttyUSB0').
    
    Returns:
        str: Response from the meter.
    """
    try:
        # Configure serial connection
        ser = serial.Serial(
            port=port,
            baudrate=300,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS,
            timeout=15
        )

        if not ser.isOpen():
            ser.open()

        print("Serial port opened.")
        
        # Send identification request
        ser.write(b"/?!\r\n")  # Send request for identification
        time.sleep(1)
        
        # Read response
        response = ser.read(100).decode('ascii')
        print("Response from meter:", response)

        # Acknowledge the meter
        ack_command = b"\x06\x30\x30\x30\x0D\x0A"  # <ACK>000<CR><LF>
        ser.write(ack_command)
        print("Sent acknowledgment.")
        time.sleep(1)

        # Read further data
        data = ser.read(375).decode('ascii')  # Adjust bytes to match expected data length
        print("Meter data:", data)

        ser.close()
        print("Serial port closed.")
        return data

    except serial.SerialException as e:
        print("Error communicating with the meter:", e)
        return None

# Example usage
port = "/dev/ttyUSB0"  # Replace with your actual port
meter_data = communicate_with_meter(port)
if meter_data:
    print("Final meter data:\n", meter_data)
