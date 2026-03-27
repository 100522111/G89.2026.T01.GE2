"""Module """
import re 
import json
from pathlib import Path
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
#general case JSON_FILES_PATH =(str(Path.home())+"/G89.2026.T01.GE2/src/main/JsonFiles")
#JSON_FILES_PATH=("C:\AAADRIANO\MIERDA SISTEMA EDUCATIVO AHHHHHHHHHHHHHHHHH\G89.2026.T01.GE2")
JSON_FILES_PATH =(r"C:\Users\raque\Downloads\Nico\G89.2026.T01.GE2\src\main\JsonFiles") #Mycase
corporate_operations=JSON_FILES_PATH+"/corporate_operations.json"
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self,company_cif: str, project_achronym: str, project_description: str, department: str,date: str, budget: float):
        if  not isinstance(company_cif, str):
           raise EnterpriseManagementException("ERROR CIF must be a string")
        #raises error if format isn't the correct one
        else:
            if self.validate_cif(company_cif) == False:
                raise EnterpriseManagementException("Invalid CIF format") #checks if the CIF is the correct format
        if  not isinstance(project_achronym, str):
           raise EnterpriseManagementException("ERROR project acronym must be a string") #checks if the acronym is the correct format (string)
        if not isinstance(department, str):
            raise EnterpriseManagementException("ERROR department must be a string") #checks if the department is the correct format (string)
        else:
            if department not in ("HR", "FINANCE", "LEGAL", "LOGISTICS"):
                raise EnterpriseManagementException("ERROR department must be one of the following strings: HR, FINANCE, LEGAL, LOGISTICS") #checks if the department is one of the valid strings

        #Get the result for t1-t4
        result = EnterpriseProject(company_cif, project_achronym, project_description, department, date, budget)
        #store into JSON

        with open(corporate_operations, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)  #We store the JSON content into a list
            except json.JSONDecodeError:
                data = []  #We check incase the JSON content is empty
        if isinstance(data, str):
            data = [data]
        paramlist=[company_cif,project_achronym,project_description,department,date,budget,result.project_id]

        data.append(paramlist) #we add our result to the list

        try:
            with open(corporate_operations, "w", encoding="utf-8", newline="") as file:
                json.dump(data,file,indent=2) #we dump the list (we did it this way because dump rewrites)


        except FileNotFoundError:
            data = []
        except json.decoder.JSONDecodeError as ex:
            raise EnterpriseManagementException("json decode error-wrong json format") from ex


        return result.project_id #return if everything worked

    """" """


    @staticmethod
    def validate_cif(cif: str):
        """
        Validates a Spanish CIF according to the Guided Exercise 1 rules.
        Format: 1 Letter - 7 Numbers - 1 Control Character
        """
        # If the CIF isn't a string, return False
        if not isinstance(cif, str):
            return False
            
        cif = cif.upper()

        # Checking format to be 1 letter + 7 digits + 1 alphanumeric control [cite: 25]
        if not re.fullmatch(r"[A-Z]\d{7}[A-Z0-9]", cif):
            return False

        letter = cif[0]
        numbers = cif[1:8] # The 7 numerical digits (Central body) [cite: 27]
        control = cif[8]

        # STEP 1: Add the digits located in the even positions of the block [cite: 31]
        # In a 7-digit block (indices 0-6), even positions are indices 1, 3, and 5
        even_sum = int(numbers[1]) + int(numbers[3]) + int(numbers[5])

        # STEP 2: Process the odd-numbered digits (indices 0, 2, 4, 6) [cite: 32]
        odd_sum = 0
        for i in [0, 2, 4, 6]:
            digit = int(numbers[i])
            # Multiply the digit by 2 [cite: 34]
            doubled = digit * 2
            # If the result has two digits, add them (e.g., 16 -> 1+6=7) 
            odd_sum += (doubled // 10) + (doubled % 10)

        # STEP 3: Add the result of step 1 + step 2 [cite: 38]
        total_sum = even_sum + odd_sum

        # STEP 4: Calculation of the Base Digit [cite: 39]
        # Obtain the unit of the Partial Sum and subtract it from 10
        unit = total_sum % 10
        # Note: If the unit is 0, the base digit is 0 
        if unit == 0:
            base_digit = 0
        else:
            base_digit = 10 - unit

        # STEP 5: Determination of the control character [cite: 41]
        # Mapping table for letters K, P, Q, S [cite: 50]
        control_letters = "JABCDEFGHI"

        if letter in "ABEH":
            # the control character is the number obtained in step 4 [cite: 43]
            return control == str(base_digit)

        if letter in "KPQS":
            # locate the value of the base digit in the table [cite: 48]
            return control == control_letters[base_digit]

        # For other organization types (C, D, F, G, J, U, V), it can be either
        return control == str(base_digit) or control == control_letters[base_digit]
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
