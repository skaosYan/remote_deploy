import unittest
import urllib.request

import sys
sys.path.append('../')

from remote import Control

CONFIG_TEST_FILE = "test_configuration.json"

class TestControl(unittest.TestCase):

    def testControl(self):
        # prepare test
        control = Control(CONFIG_TEST_FILE)
        control.install()

        # validate test
        hostname = control.json_config['hosts'][0]['hostname']
        file = control.json_config['files'][0]['filename']
        response = urllib.request.urlopen("http://"+hostname+"/"+file).read()

        self.assertEqual(response, b'Hello, world!\n', 'HTTP response is wrong!')

if __name__ == '__main__':
    unittest.main()
