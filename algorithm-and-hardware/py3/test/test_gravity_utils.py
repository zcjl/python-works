# -*- coding: utf-8 -*-

import unittest
from unittest import mock
import json
from gravity_utils import *


class TestGravityUtils(unittest.TestCase):
    """Test mathfuc.py"""

    def setUp(self):
        self.util = GravityUtils()
        self.util.ports = {
            "g_sensor_1": serial.Serial(port='/dev/ttys1', timeout=0.04)
            # "g_sensor_2": serial.Serial(port='/dev/ttys2', timeout=0.04),
            # "g_sensor_3": serial.Serial(port='/dev/ttys2', timeout=0.04),
            # "g_sensor_4": serial.Serial(port='/dev/ttys3', timeout=0.04)
        }
        self.util.offset = 100

    def tearDown(self):
        # print "do something after test.Clean up."
        pass

    def test_read(self):
        serial.Serial.read = mock.Mock(return_value=b'\x2B\x20\x20\x31\x30\x30\x0D\x0A')
        result = self.util.read_gravity()
        self.assertTrue(result['success'])
        self.assertEqual(0, result['data']['g_sensor_1'])

    def test_convert_data(self):
        """Test method convert_data(binary_data)"""
        self.assertEqual(0, self.util.convert_binary(b'\x20\x20\x20\x20\x30'))  # empty_dish
        self.assertEqual(10, self.util.convert_binary(b'\x20\x20\x20\x31\x30'))  # 10g
        self.assertEqual(20, self.util.convert_binary(b'\x20\x20\x20\x32\x30'))  # 20g
        self.assertEqual(50, self.util.convert_binary(b'\x20\x20\x20\x35\x30'))  # 50g
        self.assertEqual(100, self.util.convert_binary(b'\x20\x20\x31\x30\x30'))  # 100g
        self.assertEqual(200, self.util.convert_binary(b'\x20\x20\x32\x30\x30'))  # 200g
        self.assertEqual(300, self.util.convert_binary(b'\x20\x20\x33\x30\x30'))  # 300g
        self.assertEqual(400, self.util.convert_binary(b'\x20\x20\x34\x30\x30'))  # 400g
        self.assertEqual(500, self.util.convert_binary(b'\x20\x20\x35\x30\x30'))  # 500g
        self.assertEqual(600, self.util.convert_binary(b'\x20\x20\x36\x30\x30'))  # 600g
        self.assertEqual(700, self.util.convert_binary(b'\x20\x20\x37\x30\x30'))  # 700g
        self.assertEqual(800, self.util.convert_binary(b'\x20\x20\x38\x30\x30'))  # 800g
        self.assertEqual(900, self.util.convert_binary(b'\x20\x20\x39\x30\x30'))  # 900g
        self.assertEqual(1000, self.util.convert_binary(b'\x20\x31\x30\x30\x30'))  # 1kg
        self.assertEqual(2000, self.util.convert_binary(b'\x20\x32\x30\x30\x30'))  # 2kg
        self.assertEqual(3000, self.util.convert_binary(b'\x20\x33\x30\x30\x30'))  # 3kg
        self.assertEqual(5000, self.util.convert_binary(b'\x20\x35\x30\x30\x30'))  # 5kg
        self.assertEqual(6000, self.util.convert_binary(b'\x20\x36\x30\x30\x30'))  # 6kg
        self.assertEqual(7000, self.util.convert_binary(b'\x20\x37\x30\x30\x30'))  # 7kg
        self.assertEqual(8000, self.util.convert_binary(b'\x20\x38\x30\x30\x30'))  # 8kg
        self.assertEqual(10000, self.util.convert_binary(b'\x31\x30\x30\x30\x30'))  # 10kg

    def test_convert_gravity(self):
        """Test method convert_gravity(binary_data)"""
        self.assertEqual(0, self.util.convert_gravity(b'\x2B\x20\x20\x31\x30\x30\x0D\x0A')[1])      # empty_dish
        self.assertEqual(10, self.util.convert_gravity(b'\x2B\x20\x20\x31\x31\x30\x0D\x0A')[1])     # 10g
        self.assertEqual(20, self.util.convert_gravity(b'\x2B\x20\x20\x31\x32\x30\x0D\x0A')[1])     # 20g
        self.assertEqual(50, self.util.convert_gravity(b'\x2B\x20\x20\x31\x35\x30\x0D\x0A')[1])     # 50g
        self.assertEqual(100, self.util.convert_gravity(b'\x2B\x20\x20\x32\x30\x30\x0D\x0A')[1])    # 100g
        self.assertEqual(200, self.util.convert_gravity(b'\x2B\x20\x20\x33\x30\x30\x0D\x0A')[1])    # 200g
        self.assertEqual(300, self.util.convert_gravity(b'\x2B\x20\x20\x34\x30\x30\x0D\x0A')[1])    # 300g
        self.assertEqual(400, self.util.convert_gravity(b'\x2B\x20\x20\x35\x30\x30\x0D\x0A')[1])    # 400g
        self.assertEqual(500, self.util.convert_gravity(b'\x2B\x20\x20\x36\x30\x30\x0D\x0A')[1])    # 500g
        self.assertEqual(600, self.util.convert_gravity(b'\x2B\x20\x20\x37\x30\x30\x0D\x0A')[1])    # 600g
        self.assertEqual(700, self.util.convert_gravity(b'\x2B\x20\x20\x38\x30\x30\x0D\x0A')[1])    # 700g
        self.assertEqual(800, self.util.convert_gravity(b'\x2B\x20\x20\x39\x30\x30\x0D\x0A')[1])    # 800g
        self.assertEqual(900, self.util.convert_gravity(b'\x2B\x20\x31\x30\x30\x30\x0D\x0A')[1])    # 900g
        self.assertEqual(1000, self.util.convert_gravity(b'\x2B\x20\x31\x31\x30\x30\x0D\x0A')[1])   # 1kg
        self.assertEqual(2000, self.util.convert_gravity(b'\x2B\x20\x32\x31\x30\x30\x0D\x0A')[1])   # 2kg
        self.assertEqual(3000, self.util.convert_gravity(b'\x2B\x20\x33\x31\x30\x30\x0D\x0A')[1])   # 3kg
        self.assertEqual(5000, self.util.convert_gravity(b'\x2B\x20\x35\x31\x30\x30\x0D\x0A')[1])   # 5kg
        self.assertEqual(6000, self.util.convert_gravity(b'\x2B\x20\x36\x31\x30\x30\x0D\x0A')[1])   # 6kg
        self.assertEqual(7000, self.util.convert_gravity(b'\x2B\x20\x37\x31\x30\x30\x0D\x0A')[1])   # 7kg
        self.assertEqual(8000, self.util.convert_gravity(b'\x2B\x20\x38\x31\x30\x30\x0D\x0A')[1])   # 8kg
        self.assertEqual(10000, self.util.convert_gravity(b'\x2B\x31\x30\x31\x30\x30\x0D\x0A')[1])  # 10kg

        self.assertEqual(6695, self.util.convert_gravity(b'\x2B\x20\x36\x37\x39\x35\x0D\x0A')[1])   # 6695g
        self.assertEqual(6696, self.util.convert_gravity(b'\x2B\x20\x36\x37\x39\x36\x0D\x0A')[1])   # 6696g

        # 标示位错误
        self.assertEqual((False, GravityUtils.Code.MARK), self.util.convert_gravity(b'\x2C\x20\x39\x39\x39\x30\x0D\x0A'))
        # 校验位错误
        self.assertEqual((False, GravityUtils.Code.CHECK), self.util.convert_gravity(b'\x2B\x31\x30\x30\x30\x30\x0C\x0A'))


if __name__ == '__main__':
    unittest.main()
