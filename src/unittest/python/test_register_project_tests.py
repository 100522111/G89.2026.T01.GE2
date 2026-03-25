"""class for testing the regsiter_order method"""
import sys
import os

# We get to the absolute path so we can import everything
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "main", "python"))

# We put the path on top of the path list
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# we import
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.project_document import ProjectDocument
from freezegun import freeze_time
import unittest


class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    def test_something( self ):
        """dummy test"""
        self.assertEqual(True, False)
    def test_TC1(self):

        o=EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result=o.register_project(company_cif="Z54712541",project_achronym="ABCDE",project_description="10_char_de",department="HR",date="1/1/2025",budget=50000.00)

        self.assertEqual(result,"e002cdc5ce02bb0873afd10160dc864e")

    def test_TC2(self):
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("A12345678","EMIGRATING","this_description_has_30_charas","FINANCE","31/12/2027",10000)
        self.assertEqual(result, "5e9c1747169161b86c7e968a23bdaafe")
    def test_TC3(self):
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("V8321393","CLOUDPYT","moving to cloud"	,"LEGAL","20/02/2026",1000000)
        self.assertEqual(result, "e549a73b0e348ec0e63fa82e6142928c")
    def test_TC4(self):
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("B34798256","CLOUDPYT","moving to cloud","LOGISTICS","1/12/2025",50000)
        self.assertEqual(result, "7562f75b44b153538d1af9cac72feb7f")

if __name__ == '__main__':
    unittest.main()
