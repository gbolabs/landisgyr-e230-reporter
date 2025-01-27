import serial
import time

def connect_to_meter(port, baudrate):
    """
    Connect to the meter using a serial interface.
    :param port: The COM port of the optical interface (e.g., 'COM3', '/dev/ttyUSB0').
    :param baudrate: Communication speed, typically 300 or 9600 for IEC 1107.
    :return: Serial connection object.
    """
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        print("Connected to meter.")
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")
        return None

def handshake(serial_connection):
    """
    Perform the IEC 1107 handshake to initiate communication.
    :param serial_connection: The serial connection object.
    """
    try:
        # Send the initial request "/?!<CR><LF>" to wake up the meter
        serial_connection.write(b"/?!\r\n")
        time.sleep(0.5)
        
        # Read the response
        response = serial_connection.read(100).decode('ascii', errors='ignore')
        print(f"Handshake response: {response}")
        
        # Send ACK (acknowledgment) to proceed with data transfer (assuming '2' baudrate switch command)
        serial_connection.write(b"\x06" + b"2" + b"\r\n")
        time.sleep(0.5)

        # Read the meter's data stream
        data_stream = serial_connection.read(500).decode('ascii', errors='ignore')
        print(f"Meter data: {data_stream}")
    except Exception as e:
        print(f"Error during handshake: {e}")

def main():
    # Replace 'COM3' with the correct port for your optical reader
    port = '/dev/ttyUSB1'  # Windows example, or '/dev/ttyUSB0' for Linux
    baudrate = 300  # Start with the initial baudrate defined by the meter

    # Connect to the meter
    serial_connection = connect_to_meter(port, baudrate)
    if serial_connection:
        try:
            # Perform handshake and read data
            handshake(serial_connection)
        finally:
            # Always close the serial connection when done
            serial_connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
