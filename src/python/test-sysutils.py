import logging
import unittest

from sysutils import Sysutils


class TestSysUtils(unittest.TestCase):

    def test_isEnergyMeterNode(self):
        import sysutils
        import platform

        sysutils = Sysutils()
        result = sysutils.IsEnergyMeterNode()
        node_name = platform.node()

        if node_name == sysutils.RPI_EM_NODE_NAME:
            self.assertTrue(result)
        else:
            self.assertFalse(result)

    def test_givenNodeNameIsRaspberryPi_expectTrue(self):
        import sysutils
        import platform

        sysutils = Sysutils(Sysutils.RPI_EM_NODE_NAME)
        result = sysutils.IsEnergyMeterNode()
        node_name = platform.node()

        self.assertTrue(result)

    def test_givenNodeNameIsRaspberryPi_expectFalse(self):
        import sysutils
        import platform

        sysutils = Sysutils("Not raspberrypi")
        result = sysutils.IsEnergyMeterNode()
        node_name = platform.node()

        self.assertFalse(result)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    unittest.main()
