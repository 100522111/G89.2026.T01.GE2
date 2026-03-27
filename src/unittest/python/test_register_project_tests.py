"""class for testing the regsiter_order method"""
import sys
import os
import json
import unittest
#from src.main.python.uc3m_consulting import JSON_FILES_PATH
# we import
#pylint: disable=wrong-import-position
from pathlib import Path
from freezegun import freeze_time
# We get to the absolute path so we can import everything
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "main", "python"))

# We put the path on top of the path list
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
#pylint: enable=wrong-import-position

#general case JSON_FILES_PATH =(str(Path.home())+"/G89.2026.T01.GE2/src/main/JsonFiles")
JSON_FILES_PATH="C:/AAADRIANO/MIERDA SISTEMA EDUCATIVO AHHHHHHHHHHHHHHHHH/G89.2026.T01.GE2"
#JSON_FILES_PATH =r"C:/Users/raque/Downloads/Nico/G89.2026.T01.GE2/src/main/JsonFiles" #Mycase
CORPORATE_OPERATIONS= JSON_FILES_PATH + "/corporate_operations.json"

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    def setUp(self):
        """This runs automatically before every test to provide a clean slate."""
        with open(CORPORATE_OPERATIONS, "w", encoding="utf-8") as file:
            json.dump([], file)  # leaves the JSON blank for next test

    @classmethod
    def tearDownClass(cls):
        """This runs onmy once after all tests are finished"""

        #Wipe the file clean
        with open(CORPORATE_OPERATIONS, "w", encoding="utf-8") as file:
            json.dump([], file)

        #Register the 4 valid projects
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            o.register_project("B98765431", "ABCDE", "10_char_de", "HR", "01/01/2025", 50000.01)  # TC1
            o.register_project("A12345674", "EMIGRATING", "this_description_has_30_charas", "FINANCE", "31/12/2027",100000.00)  # TC2
            o.register_project("P3900004G", "CLOUDPYT", "moving to cloud", "LEGAL", "20/02/2026", 1000000.00)  # TC3
            o.register_project("B34798256", "CLOUDPYT", "moving to cloud", "LOGISTICS", "1/12/2025", 50000.01)  # TC4

    def test_tc1(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o=EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result=o.register_project(company_cif="B98765431",project_achronym="ABCDE",project_description="10_char_de",department="HR",date="01/01/2025",budget=50000.01)

        self.assertEqual(result,"8c3b05cc90c582dfdb8b47bf41c7c7ae")
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8", newline="") as file: #we open the file to check if it has been saved
            data_list=json.load(file)
        found= False
        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            if "B98765431" in str(item):
                found = True
        self.assertTrue(found)

    def test_tc2(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("A12345674","EMIGRATING","this_description_has_30_charas", "FINANCE","31/12/2027",100000.00)
        self.assertEqual(result, "92120f42918eefa12621a18a18588b44")
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8", newline="") as file:  # we open the file to check if it has been saved
            data_list = json.load(file)
        found = False
        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            if "A12345674" in str(item):
                found = True
        self.assertTrue(found)

    def test_tc3(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("P3900004G","CLOUDPYT","moving to cloud","LEGAL","20/02/2026",1000000.00)
        self.assertEqual(result, "bc098bead4214bc96df989d618ee8dac")
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been saved
            data_list = json.load(file)

        found = False
        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            if "P3900004G" in str(item):
                found = True
        self.assertTrue(found)

    def test_tc4(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("B34798256","CLOUDPYT","moving to cloud","LOGISTICS","1/12/2025",50000.01)
        self.assertEqual(result, "039c91e63c7ef7486963f80f6e4c9681")
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been saved
            data_list = json.load(file)
            print(data_list)
        found = False

        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            if "B34798256" in str(item):
                found = True
        self.assertTrue(found)

    def test_tc5(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("12345678", "...", "...", "HR", "20/02/2026", 70000.00)
        self.assertEqual(cm.exception.message, "Invalid CIF format") #we test the cif of the format
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2,data_list)#the test passes if the list workws

    def test_tc6(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project(30000000, "...", "...", "LOGISTICS", "2/12/2025", 70000.00)
        self.assertEqual(cm.exception.message, "ERROR CIF must be a string") #we test the cif of the format
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2,data_list)#the test passes if the list works

    def test_tc7(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", 300, "...", "LOGISTICS", "2/12/2025", 70000.00)
        self.assertEqual(cm.exception.message, "ERROR project acronym must be a string") #we test the acronym of the format
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2,data_list)#the test passes if the list works

    def test_tc8(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", 300, "3/12/2025", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR department must be a string")  # we test the department of the format (string)
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc9(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "MARKETING", "3/12/2025", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR department must be one of the following strings: HR, FINANCE, LEGAL, LOGISTICS")  # we test the format of the department
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc10(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", 4/12/2025, 50000.02)
        self.assertEqual(cm.exception.message, "ERROR date must be a string")  # we test the format of the date
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc11(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "Jose Luis", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR date format must be DD/MM/YYYY")  # we test the format of the date
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc12(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "05/12/2025", "5 potatoes")
        self.assertEqual(cm.exception.message, "ERROR budget must be a float")  # we test the format of the date
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc13(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "00/00/2023", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR date format must be DD/MM/YYYY")  # we test the format of the date
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc14(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "05/12/2025", 60000.123)
        self.assertEqual(cm.exception.message, "ERROR budget cannot have more than 2 decimals")  # we test the format of the budget
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc15(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "05/12/2025", 6000.00)
        self.assertEqual(cm.exception.message, "ERROR budget must be higher than 50000.00")  # we test the format of the budget
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc16(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "05/12/2025", 7000000.03)
        self.assertEqual(cm.exception.message, "ERROR budget must be lower than 1000000.00")  # we test the format of the budget
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc17(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", 300, "LOGISTICS", "05/12/2025", 50000.05)
        self.assertEqual(cm.exception.message, "ERROR project_description must be a string")  # we test the format of the description
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc18(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "hi", "LOGISTICS", "05/12/2025", 50000.05)
        self.assertEqual(cm.exception.message, "ERROR project description must be between 10 and 30 characters")  # we test the format of the description
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc19(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "this description is veryyyy long", "LOGISTICS", "05/12/2025", 50000.05)
        self.assertEqual(cm.exception.message, "ERROR project description must be between 10 and 30 characters")  # we test the format of the description
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc20(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "HI", "...", "LOGISTICS", "05/12/2025", 50000.05)
        self.assertEqual(cm.exception.message, "ERROR project acronym must be between 5 and 10 characters")  # we test the format of the description
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc21(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "TRISKADEIKAPHOBIA", "...", "LOGISTICS", "05/12/2025", 50000.05)
        self.assertEqual(cm.exception.message, "ERROR project acronym must be between 5 and 10 characters")  # we test the format of the description
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc22(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "32/13/2028", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR date format must be DD/MM/YYYY")  # we test the format of the date
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc23(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "@@@@@@", "project description", "LOGISTICS", "05/12/2025", 50000.05)
        self.assertEqual(cm.exception.message, "ERROR project acronym contains invalid characters")  # we test the format of the description
        with open(CORPORATE_OPERATIONS, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)

        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc24(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()

        with freeze_time("2025-01-12 12:00:00"):
            o.register_project("A58818501", "DUPTEST", "valid_description", "HR", "01/01/2025", 50000.00)


        with self.assertRaises(EnterpriseManagementException) as cm: #Try to register a project with the same CIF and acronym (invalid output)
            with freeze_time("2025-01-12 12:05:00"):
                #We use the same CIF ("A58818501") and Acronym ("DUPTEST")
                o.register_project("A58818501", "DUPTEST", "different_desc", "FINANCE", "02/01/2025", 60000.00)

        self.assertEqual(cm.exception.message, "ERROR: A project with this name and CIF already exists")

    def test_tc25(self):
        """WE APPLY THE TEST DEFINED ON THE EXCEL """
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("A58818501", "ABCDE", "10_char_de", "HR", "01/01/2025", 50000.01)

        #Check that the output is a string
        self.assertIsInstance(result, str, "The output is not a string")

        #Check that it is exactly 32 chars long
        self.assertEqual(len(result), 32, f"Expected 32 chars, but got {len(result)}")

        self.assertEqual(result, "ebd95e367693cbb592170c1e077cc8ac")

if __name__ == '__main__':
    unittest.main()
