from io import FileIO
from sysutils import Sysutils
import processdata
import azureclient
import logging


def read_fromMock() -> str:
    try:
        f = open('mockdata.txt', mode='r')
        lines = f.read()
        logging.info("Read "+lines.__len__+" lines to be used as mock")
    except Exception:
        logging.error('Unable to read mock information')
        raise

def read_fromSerial() -> str:
    import time
    import serial

    READ_BYTES = 375
    READ_TIMEOUT_SEC = 15

    # Serial takes two parameters: serial device and baudrate
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=300,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=READ_TIMEOUT_SEC,
        xonxoff=False,
        rtscts=False,
    )

    if (not ser.isOpen()):
        ser.open()
        logging.info("Serial port open")

    if (ser.isOpen()):
        logging.info("Serial port open, writing...")
        command = b"\x2F\x3F\x21\x0D\x0A"  # /?!<CRL><LF>
        logging.info("/?!<CRL><LF> : "+str(command))
        ser.write(command)
        time.sleep(1)
        command = b"\x06\x30\x30\x30\x0D\x0A"  # <ACK>000<CR><LF>
        logging.info("<ACK>000<CR><LF> : "+str(command))
        ser.write(command)

        logging.info(
            "Wait for 1s in order to let the serialport completes the write")

        time.sleep(1)

        logging.info("Reading.. {} block from serial".format(READ_BYTES))
        start = time.time()
        data = ser.read(READ_BYTES)
        delta = time.time()-start
        logging.info("Reading "+str(data.__len__())+" took "+str(delta))

        ser.close()
        logging.info("Serial port closed")

        return data


# Configure logging
logging.basicConfig(filename="/var/log/energy-meter/ingress.log",
                    filemode='w', level=logging.DEBUG)

if Sysutils().IsEnergyMeterNode():
    data = read_fromSerial()
else:
    data = read_fromMock()

paresdData = processdata.parse_powermeter_data(data)

azureclient.post_to_azure_read_info(paresdData)
