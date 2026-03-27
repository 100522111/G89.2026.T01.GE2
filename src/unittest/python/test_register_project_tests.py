"""class for testing the regsiter_order method"""
import sys
import os
import json
#from src.main.python.uc3m_consulting import JSON_FILES_PATH
# we import
from freezegun import freeze_time
import unittest
import json
from pathlib import Path

# We get to the absolute path so we can import everything
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "main", "python"))

# We put the path on top of the path list
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument

#general case JSON_FILES_PATH =(str(Path.home())+"/G89.2026.T01.GE2/src/main/JsonFiles")
#JSON_FILES_PATH=("C:\AAADRIANO\MIERDA SISTEMA EDUCATIVO AHHHHHHHHHHHHHHHHH\G89.2026.T01.GE2")
JSON_FILES_PATH =(r"C:\Users\raque\Downloads\Nico\G89.2026.T01.GE2\src\main\JsonFiles") #Mycase
corporate_operations=JSON_FILES_PATH+"/corporate_operations.json"

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""


    def test_tc1(self):

        o=EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result=o.register_project(company_cif="A58818501",project_achronym="ABCDE",project_description="10_char_de",department="HR",date="01/01/2025",budget=50000.00)

        self.assertEqual(result,"c07f9592c27f8d90ca764cbd3f869702")
        with open(corporate_operations,"r",encoding= "utf-8",newline="") as file: #we open the file to check if it has been saved
            data_list=json.load(file)
        found= False
        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            for a in item: #since we store things as a list of lists, we have to do this
                if a == result:
                    found = True
        self.assertTrue(found)

    def test_tc2(self):
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("A12345674","EMIGRATING","this_description_has_30_charas", "FINANCE","31/12/2027",10000)
        self.assertEqual(result, "235c24d9bdf837fe5f05f9c3d45f1b31")
        with open(corporate_operations, "r", encoding="utf-8", newline="") as file:  # we open the file to check if it has been saved
            data_list = json.load(file)
        found = False
        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            for a in item: #since we store things as a list of lists, we have to do this
                if a == result:
                    found = True
        self.assertTrue(found)

    def test_tc3(self):
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("P3900004G","CLOUDPYT","moving to cloud","LEGAL","20/02/2026",1000000)
        self.assertEqual(result, "a68979499be6f81f79402d54a21ec871")
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been saved
            data_list = json.load(file)

        found = False
        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            for a in item: #since we store things as a list of lists, we have to do this
                if a == result:
                    found = True
        self.assertTrue(found)

    def test_tc4(self):
        o = EnterpriseManager()
        with freeze_time("2025-01-12 12:00:00"):
            result = o.register_project("B34798256","CLOUDPYT","moving to cloud","LOGISTICS","1/12/2025",50000)
        self.assertEqual(result, "7562f75b44b153538d1af9cac72feb7f")
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been saved
            data_list = json.load(file)

        found = False

        for item in data_list:  # we check the file (it is a list of id's) to see if the id is there
            for a in item:
                if a == result:
                    found = True
        self.assertTrue(found)

    def test_tc5(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("12345678", "...", "...", "HR", "20/02/2026", 70000)
        self.assertEqual(cm.exception.message, "Invalid CIF format") #we test the cif of the format
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2,data_list)#the test passes if the list workws

    def test_tc6(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project(30000000, "...", "...", "LOGISTICS", "2/12/2025", 70000)
        self.assertEqual(cm.exception.message, "ERROR CIF must be a string") #we test the cif of the format
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2,data_list)#the test passes if the list works

    def test_tc7(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", 300, "...", "LOGISTICS", "2/12/2025", 70000)
        self.assertEqual(cm.exception.message, "ERROR project acronym must be a string") #we test the acronym of the format
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2,data_list)#the test passes if the list works

    def test_tc8(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", 300, "3/12/2025", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR department must be a string")  # we test the department of the format (string)
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc9(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "MARKETING", "3/12/2025", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR department must be one of the following strings: HR, FINANCE, LEGAL, LOGISTICS")  # we test the format of the department
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc10(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", 4/12/2025, 50000.02)
        self.assertEqual(cm.exception.message, "ERROR date must be a string")  # we test the format of the date
        with open(corporate_operations, "r", encoding="utf-8",
        newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

    def test_tc11(self):
        o = EnterpriseManager()
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file before calling the function
            data_list = json.load(file)
        with self.assertRaises(EnterpriseManagementException) as cm:
            o.register_project("A58818501", "CLOUDPYT", "...", "LOGISTICS", "Jose Luis", 50000.02)
        self.assertEqual(cm.exception.message, "ERROR date format must be DD/MM/YYYY")  # we test the format of the date
        with open(corporate_operations, "r", encoding="utf-8",
                  newline="") as file:  # we open the file to check if it has been changed
            data_list2 = json.load(file)
        self.assertEqual(data_list2, data_list)  # the test passes if the list works

if __name__ == '__main__':
    unittest.main()
