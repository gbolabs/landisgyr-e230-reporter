import platform
from flask import Flask, jsonify, request
import time
import re
from datetime import datetime

def is_raspberry_pi():
    """
    Detect if the system is running on a Raspberry Pi by reading `/proc/cpuinfo`.
    """
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'raspberrypi' in cpuinfo.lower():
                return True
    except FileNotFoundError:
        pass  # If /proc/cpuinfo is not found, it's not a Raspberry Pi

    return False

if is_raspberry_pi():
    import serial  # Use real serial communication on Raspberry Pi
else:
    # Mock serial for non-Raspberry Pi environments
    class MockSerial:
        PARITY_EVEN = "E"
        STOPBITS_ONE = 1
        SEVENBITS = 7
        
        @staticmethod
        def Serial(*args, **kwargs):
            # Mimic the behavior of the real serial.Serial constructor
            return MockSerial(*args, **kwargs)

        def __init__(self, *args, **kwargs):
            # Initialization to mimic the real serial object
            self.port = kwargs.get('port', '/dev/ttyUSB0')
            self.baudrate = kwargs.get('baudrate', 300)
            self.timeout = kwargs.get('timeout', 15)
            print(f"MockSerial initialized with port {self.port}, baudrate {self.baudrate}")

        def open(self):
            print(f"Mock serial port opened on {self.port}.")

        def isOpen(self):
            return True

        def write(self, data):
            print(f"Mock write: {data}")

        def read(self, size):
            time.sleep(1)  # Simulate read delay
            with open('mock-data.txt', 'r') as file:
                return file.read(size).encode()  # Return data as bytes

        def close(self):
            print("Mock serial port closed.")

    serial = MockSerial  # Replace serial with mock implementation

# Flask app setup
app = Flask(__name__)

@app.route('/api/meters/<meter_id>/measure', methods=['GET'])
def get_meter_measure(meter_id):
    """
    API endpoint to retrieve measurement data for a specific meter.
    If running on Raspberry Pi, reads real serial data; otherwise, uses mock data.
    
    Parameters:
        meter_id (str): ID of the meter for which data is requested.
    
    Returns:
        JSON response containing meter data or an error message.
    """
    if isinstance(serial, MockSerial):
        # Return mock data when not running on RPI
        meter_data = MOCK_METER_DATA.get(meter_id)
        if meter_data:
            return jsonify({"meter_id": meter_id, "data": meter_data}), 200
        else:
            return jsonify({"error": f"No data found for meter ID '{meter_id}'"}), 404
    else:
        # Read data from real serial port on Raspberry Pi
        try:
            ser = serial.Serial(
                port=f'/dev/ttyUSB{meter_id}',
                baudrate=300,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.SEVENBITS,
                timeout=15,
                xonxoff=False,
                rtscts=False,
            )
            if not ser.isOpen():
                ser.open()

            # Send commands to retrieve meter data
            ser.write(b"\x2F\x3F\x21\x0D\x0A")  # /?!<CRL><LF>
            time.sleep(1)
            ser.write(b"\x06\x30\x30\x30\x0D\x0A")  # <ACK>000<CR><LF>
            time.sleep(1)
            data = ser.read(375)  # Read 375 bytes of data
            ser.close()

            pattern = r"(1\.8\.[012])\(([\d\.]+)\*kWh\)"
            decoded_data = data.decode('utf-8')

            # Find all matches
            matches = re.findall(pattern, decoded_data)

            # Display the results
            result = {match[0]: match[1] for match in matches}
        
            # Get the current date and time in ISO format
            measure_datetime = datetime.utcnow().replace(microsecond=0).isoformat() + '+00:00'

            return jsonify({"meter_id": meter_id, "decoded_data": result, "measure_datetime": measure_datetime}), 200

        except Exception as e:
            return jsonify({"error": f"Failed to read from serial: {e}"}), 500

