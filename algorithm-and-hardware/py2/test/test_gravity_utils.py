# -*- coding: utf-8 -*-

import unittest
import json
from gravity_utils import *


class TestGravityUtils(unittest.TestCase):
    """Test mathfuc.py"""

    def setUp(self):
        # print "do something before test.Prepare environment."
        pass

    def tearDown(self):
        # print "do something after test.Clean up."
        pass

    # def test_read(self):
    #     util = GravityUtils()
    #     result = util.read_gravity()
    #     print(result.errorMsg)
    #     print(json.dumps(result.__dict__))

    def test_convert_data(self):
        """Test method convert_data(binary_data)"""
        util = GravityUtils()
        self.assertEqual(376632, self.util.convert_binary(b'\x20\x33\x33\x30\x34'))  # empty_dish
        self.assertEqual(376642, self.util.convert_binary(b'\x20\x33\x33\x31\x34'))  # 10g
        self.assertEqual(376652, self.util.convert_binary(b'\x20\x33\x33\x32\x34'))  # 20g
        self.assertEqual(376682, self.util.convert_binary(b'\x20\x33\x33\x35\x34'))  # 50g
        self.assertEqual(376732, self.util.convert_binary(b'\x20\x33\x34\x30\x34'))  # 100g
        self.assertEqual(376832, self.util.convert_binary(b'\x20\x33\x35\x30\x34'))  # 200g
        self.assertEqual(376932, self.util.convert_binary(b'\x20\x33\x36\x30\x34'))  # 300g
        self.assertEqual(377032, self.util.convert_binary(b'\x20\x33\x37\x30\x34'))  # 400g
        self.assertEqual(377132, self.util.convert_binary(b'\x20\x33\x38\x30\x34'))  # 500g
        self.assertEqual(377232, self.util.convert_binary(b'\x20\x33\x39\x30\x34'))  # 600g
        self.assertEqual(377332, self.util.convert_binary(b'\x20\x34\x30\x30\x34'))  # 700g
        self.assertEqual(377432, self.util.convert_binary(b'\x20\x34\x31\x30\x34'))  # 800g
        self.assertEqual(377532, self.util.convert_binary(b'\x20\x34\x32\x30\x34'))  # 900g
        self.assertEqual(377632, self.util.convert_binary(b'\x20\x34\x33\x30\x34'))  # 1kg
        self.assertEqual(378632, self.util.convert_binary(b'\x20\x35\x33\x30\x34'))  # 2kg
        self.assertEqual(379632, self.util.convert_binary(b'\x20\x36\x33\x30\x34'))  # 3kg
        self.assertEqual(381632, self.util.convert_binary(b'\x20\x38\x33\x30\x34'))  # 5kg
        self.assertEqual(382632, self.util.convert_binary(b'\x20\x39\x33\x30\x34'))  # 6kg
        self.assertEqual(543632, self.util.convert_binary(b'\x31\x30\x33\x30\x34'))  # 7kg
        self.assertEqual(544632, self.util.convert_binary(b'\x31\x31\x33\x30\x34'))  # 8kg
        self.assertEqual(546632, self.util.convert_binary(b'\x31\x33\x33\x30\x34'))  # 10kg

    def test_convert_gravity(self):
        """Test method convert_gravity(binary_data)"""
        util = GravityUtils()
        self.assertEqual(0, self.util.convert_gravity(b'\x2B\x20\x33\x33\x30\x34\x0D\x0A')[1])      # empty_dish
        self.assertEqual(10, self.util.convert_gravity(b'\x2B\x20\x33\x33\x31\x34\x0D\x0A')[1])     # 10g
        self.assertEqual(20, self.util.convert_gravity(b'\x2B\x20\x33\x33\x32\x34\x0D\x0A')[1])     # 20g
        self.assertEqual(50, self.util.convert_gravity(b'\x2B\x20\x33\x33\x35\x34\x0D\x0A')[1])     # 50g
        self.assertEqual(100, self.util.convert_gravity(b'\x2B\x20\x33\x34\x30\x34\x0D\x0A')[1])    # 100g
        self.assertEqual(200, self.util.convert_gravity(b'\x2B\x20\x33\x35\x30\x34\x0D\x0A')[1])    # 200g
        self.assertEqual(300, self.util.convert_gravity(b'\x2B\x20\x33\x36\x30\x34\x0D\x0A')[1])    # 300g
        self.assertEqual(400, self.util.convert_gravity(b'\x2B\x20\x33\x37\x30\x34\x0D\x0A')[1])    # 400g
        self.assertEqual(500, self.util.convert_gravity(b'\x2B\x20\x33\x38\x30\x34\x0D\x0A')[1])    # 500g
        self.assertEqual(600, self.util.convert_gravity(b'\x2B\x20\x33\x39\x30\x34\x0D\x0A')[1])    # 600g
        self.assertEqual(700, self.util.convert_gravity(b'\x2B\x20\x34\x30\x30\x34\x0D\x0A')[1])    # 700g
        self.assertEqual(800, self.util.convert_gravity(b'\x2B\x20\x34\x31\x30\x34\x0D\x0A')[1])    # 800g
        self.assertEqual(900, self.util.convert_gravity(b'\x2B\x20\x34\x32\x30\x34\x0D\x0A')[1])    # 900g
        self.assertEqual(1000, self.util.convert_gravity(b'\x2B\x20\x34\x33\x30\x34\x0D\x0A')[1])   # 1kg
        self.assertEqual(2000, self.util.convert_gravity(b'\x2B\x20\x35\x33\x30\x34\x0D\x0A')[1])   # 2kg
        self.assertEqual(3000, self.util.convert_gravity(b'\x2B\x20\x36\x33\x30\x34\x0D\x0A')[1])   # 3kg
        self.assertEqual(5000, self.util.convert_gravity(b'\x2B\x20\x38\x33\x30\x34\x0D\x0A')[1])   # 5kg
        self.assertEqual(6000, self.util.convert_gravity(b'\x2B\x20\x39\x33\x30\x34\x0D\x0A')[1])   # 6kg
        self.assertEqual(7000, self.util.convert_gravity(b'\x2B\x31\x30\x33\x30\x34\x0D\x0A')[1])   # 7kg
        self.assertEqual(8000, self.util.convert_gravity(b'\x2B\x31\x31\x33\x30\x34\x0D\x0A')[1])   # 8kg
        self.assertEqual(10000, self.util.convert_gravity(b'\x2B\x31\x33\x33\x30\x34\x0D\x0A')[1])  # 10kg

        self.assertEqual(6695, self.util.convert_gravity(b'\x2B\x20\x39\x39\x39\x39\x0D\x0A')[1])   # 6695g
        self.assertEqual(6696, self.util.convert_gravity(b'\x2B\x31\x30\x30\x30\x30\x0D\x0A')[1])   # 6696g

        # 数据位数错误
        self.assertEqual((False, ApiResult.Code.LEN), self.util.convert_gravity(b''))
        # 标示位错误
        self.assertEqual((False, ApiResult.Code.MARK), self.util.convert_gravity(b'\x2C\x20\x39\x39\x39\x39\x0D\x0A'))
        # 校验位错误
        self.assertEqual((False, ApiResult.Code.CHECK), self.util.convert_gravity(b'\x2B\x31\x30\x30\x30\x30\x0C\x0A'))


if __name__ == '__main__':
    unittest.main()
