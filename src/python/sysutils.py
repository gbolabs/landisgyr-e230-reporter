import logging
import platform


def IsRaspberryPi() -> bool:
    import platform
    if platform.node() == "rpi-em":
        return True
    else:
        return False


log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)
logging.info("System is RaspberryPi: "+str(IsRaspberryPi()))
logging.info("System node name: "+platform.node())
