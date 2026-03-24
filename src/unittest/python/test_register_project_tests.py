"""class for testing the regsiter_order method"""
import unittest
from uc3m_consulting import EnterpriseManager

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    def test_something( self ):
        """dummy test"""
        self.assertEqual(True, False)
    def test_TC1(self):
        o=EnterpriseManager()
        result=o.register_project("Z54712541","ABCDE","10_char_de","HR",'1/1/2025',50000.00)

        self.assertEqual(result,"af6c439801893f25b2d1d023ea9fe470")

if __name__ == '__main__':
    unittest.main()
