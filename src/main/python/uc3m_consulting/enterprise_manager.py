"""Module """
import json
from pathlib import Path
from .enterprise_management_exception import EnterpriseManagementException
from .enterprise_project import EnterpriseProject
#general case JSON_FILES_PATH =(str(Path.home())+"/G89.2026.T01.GE2/src/main/JsonFiles")
JSON_FILES_PATH =(r"C:\Users\raque\Downloads\Nico\G89.2026.T01.GE2\src\main\JsonFiles") #Mycase
corporate_operations=JSON_FILES_PATH+"/corporate_operations.json"
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self,company_cif: str, project_achronym: str, project_description: str, department: str,date: str, budget: float):
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
        except json.decoder.JSONDecodeError:
            raise EnterpriseManagementException("json decode error-wrong json format") from ex


        return result.project_id #return if everything worked

    """" """


    @staticmethod
    def validate_cif(cif: str):
        """this method validates the CIF"""
        #If the CIF isn't a string, return False
        if not isinstance(cif, str):
            return False
        cif = cif.upper()

        #Checking format to be 1 letter + 7 digits + 1 alphanumeric control
        if not re.fullmatch(r"[A-Z]\d{7}[A-Z0-9]", cif):
            return False

        letter = cif[0]
        numbers = cif[1:8]
        control = cif[8]

        #Step 1: Sum even positions (2nd, 4th, 6th digits -> index 1,3,5)
        even_sum = sum(int(numbers[i]) for i in range(1, 7, 2))

        #Step 2: Process odd positions (1st, 3rd, 5th, 7th digits -> index 0,2,4,6)
        odd_sum = 0
        for i in range(0, 7, 2):
            doubled = int(numbers[i]) * 2
            if doubled > 9:
                doubled = (doubled // 10) + (doubled % 10)
            odd_sum += doubled
        #Total sum
        total_sum = even_sum + odd_sum

        #Base digit calculation
        unit = total_sum % 10
        base_digit = (10 - unit) % 10

        #Determine correct control character
        control_letters = "JABCDEFGHI"

        if letter in "ABEH":
            #Must be numeric control
            return control == str(base_digit)

        if letter in "KPQS":
            #Must be letter control
            return control == control_letters[base_digit]

        #Other letters may accept either
        return control == str(base_digit) or control == control_letters[base_digit]

        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
