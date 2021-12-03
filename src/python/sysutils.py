from typing import NoReturn


class Sysutils(object):
    RPI_EM_NODE_NAME = "rpi-em"
    _node_name_overwrite = None

    def __init__(self, node_name_overwrite: str = None) -> None:
        pass
        self._node_name_overwrite = node_name_overwrite

    def IsEnergyMeterNode(self) -> bool:
        import platform
        import logging

        if self._node_name_overwrite != None:
            node_name = self._node_name_overwrite
        else:
            node_name = platform.node()

        if node_name == self.RPI_EM_NODE_NAME:
            logging.debug("The system named '" + node_name +
                          "' IS the RaspberryPi Energy Meter.")
            return True
        else:
            logging.debug("The system named '" + node_name +
                          "' IS NOT the RaspberryPi Energy Meter.")
            return False
