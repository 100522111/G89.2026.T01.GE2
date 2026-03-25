"""UC3M CONSULTING MODULE WITH ALL THE FEATURES REQUIRED FOR ACCESS CONTROL"""
import os
from pathlib import Path
import json
JSON_FILES_PATH =(str(Path.home())+"/G89.2026.T01.GE2/src/main/JsonFiles")
corporate_operations=JSON_FILES_PATH+"/corporate_operations.json"
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_project import EnterpriseProject
