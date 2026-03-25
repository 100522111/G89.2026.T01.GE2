"""class for testing the regsiter_order method"""
import unittest
from .uc3m_consulting import EnterpriseManager

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    def test_something( self ):
        """dummy test"""
        self.assertEqual(True, False)
    def test_TC1(self):
        o=EnterpriseManager()
        result=o.register_project("Z54712541","ABCDE","10_char_de","HR",'1/1/2025',50000.00)

        self.assertEqual(result,"984daebe7981e683fdf29ba69a5b73d0")

    def test_TC2(self):
        o = EnterpriseManager()
        result = o.register_project("A12345678","EMIGRATING","this_description_has_30_charas","FINANCE","31/12/2027",10000.00)

        self.assertEqual(result, "5507ecb1047d2021ad0647db453625ef")
    def test_TC3(self):
        o = EnterpriseManager()
        result = o.register_project("V8321393","CLOUDPYT","moving to cloud"	,"LEGAL","20/02/2026",1000000.00)

        self.assertEqual(result, "956c41829ce7b413fcd28a96e294e5c5f")
    def test_TC4(self):
        o = EnterpriseManager()
        result = o.register_project("B34798256","CLOUDPYT","moving to cloud","LOGISTICS","1/12/2025",50000.00)

        self.assertEqual(result, "9c8c53f10d231ca1ce9e29671870c807")

if __name__ == '__main__':
    unittest.main()
