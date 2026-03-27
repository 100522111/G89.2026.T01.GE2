"""Module """
import re
import json
from datetime import datetime
from pathlib import Path
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject

JSON_FILES_PATH =(str(Path.home())+"/G89.2026.T01.GE2/src/main/JsonFiles")
#if this doesn't work just change it for a string containing path to jsonfiles
CORPORATE_OPERATIONS= JSON_FILES_PATH + "/corporate_operations.json"
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self,company_cif: str, project_achronym: str, project_description: str, department: str,date: str, budget: float):
        """method for registering the orders and geting a MD5 string"""
        if isinstance(company_cif, str):
            if  not validate_cif(company_cif) :
                raise EnterpriseManagementException("Invalid CIF format") #checks if the CIF is the correct format

            if  not isinstance(project_achronym, str):
                raise EnterpriseManagementException("ERROR project acronym must be a string") #checks if the acronym is the correct format (string)
            if not 5 <= len(project_achronym) <= 10:
                raise EnterpriseManagementException("ERROR project acronym must be between 5 and 10 characters") #checks if the acronym is between 5 and 10 characters
            if not re.fullmatch(r"^[a-zA-Z0-9_ ]+$", project_achronym):
                raise EnterpriseManagementException("ERROR project acronym contains invalid characters") #checks that the string only contains alphanumeric values and spaces

            if not isinstance(department, str):
                raise EnterpriseManagementException("ERROR department must be a string") #checks if the department is the correct format (string)
            if department not in ("HR", "FINANCE", "LEGAL", "LOGISTICS"):
                raise EnterpriseManagementException("ERROR department must be one of the following strings: HR, FINANCE, LEGAL, LOGISTICS") #checks if the department is one of the valid strings

            if isinstance(date, str):
                try:
                    datetime.strptime(date, "%d/%m/%Y")
                except ValueError as ex:
                    raise EnterpriseManagementException("ERROR date format must be DD/MM/YYYY") from ex #checks that date is the correct format
            else:
                raise EnterpriseManagementException("ERROR date must be a string") #checks that date is string

            if not isinstance(budget, float):
                raise EnterpriseManagementException("ERROR budget must be a float") #checks that the budget is a float
            if round(budget, 2) != budget:
                raise EnterpriseManagementException("ERROR budget cannot have more than 2 decimals") #checks if there are more than 2 decimals
            if budget < 50000.00:
                raise EnterpriseManagementException("ERROR budget must be higher than 50000.00") #checks that the budget is equal to or over 50000.00
            if budget > 1000000.00:
                raise EnterpriseManagementException("ERROR budget must be lower than 1000000.00") #checks that the budget is under 1000000.00

            if not isinstance(project_description, str):
                raise EnterpriseManagementException("ERROR project_description must be a string") #checks that the project description is a string
            if not 10 <= len(project_description) <= 30:
                raise EnterpriseManagementException("ERROR project description must be between 10 and 30 characters") #checks that the string is between 10 and 30 chars

            #Get the result for t1-t4
            result = EnterpriseProject(company_cif, project_achronym, project_description, department, date, budget)

            data = [] #Read the JSON
            try:
                with open(CORPORATE_OPERATIONS, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = [] #If the file is deleted or empty, we just start with an empty list

            if isinstance(data, str):
                data = [data]

            for item in data: #Check for duplicates
                saved_cif = item.get("_EnterpriseProject__company_cif")
                saved_name = item.get("_EnterpriseProject__project_achronym")

                if saved_cif == company_cif and saved_name == project_achronym:
                    raise EnterpriseManagementException("ERROR: A project with this name and CIF already exists")

            data.append(result.__dict__) #Save as dictionary

            #Write in the JSON file
            try:
                with open(CORPORATE_OPERATIONS, "w", encoding="utf-8", newline="") as file:
                    json.dump(data, file, indent=2)
            except Exception as ex:
                raise EnterpriseManagementException("ERROR: Could not save to JSON") from ex

            return result.project_id  # return if everything worked

        raise EnterpriseManagementException(
            "ERROR CIF must be a string")  #raises error if format isn't the correct one


def validate_cif(cif: str):
    """
    Validates a Spanish CIF according to the Guided Exercise 1 rules.
    Format: 1 Letter - 7 Numbers - 1 Control Character
    """
    # If the CIF isn't a string, return False
    if not isinstance(cif, str):
        return False
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
    #RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,OR FALSE IN OTHER CASE
