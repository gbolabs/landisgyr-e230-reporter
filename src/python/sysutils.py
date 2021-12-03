import logging
from os import environ, system
from typing import NoReturn
import sys


class Sysutils(object):
    RPI_EM_NODE_NAME = "rpi-em"
    ENERGY_METER_ENVIRONMENT = 'ENERGY_METER_ENVIRONMENT'
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

    def IsProduction(self) -> bool:
        return self.ReadEnvironment() == 'Production'

    def IsTest(self) -> bool:
        return self.ReadEnvironment() == 'Testing'

    def IsDevelopment(self) -> bool:
        return self.ReadEnvironment() == 'Development'

    def ReadEnvironment(self) -> str:
        envVar = environ.get(self.ENERGY_METER_ENVIRONMENT, None)

        argEnv = None
        for arg in sys.argv:
            if arg.startswith('-e'):
                splits = arg.split(' ')
                if splits > 1:
                    argEnv = splits[1]

        try:
            file = open('environment', mode='r')
            fileEnv = file.read()
            file.close()
        except:
            logging.error('Unable to read environment file')
            fileEnv = None

        if argEnv != None:
            return argEnv
        if fileEnv != None:
            return fileEnv
        if envVar != None:
            return envVar

        logging.error(
            "Unable to read an environment value; defaults to Development")
        
        return 'Development'
