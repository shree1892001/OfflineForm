from constant_path import *

# otp constants
APP_ID = '00939d9f-eb30-4510-b755-a733c6ae1573'
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
MsGraphJsonPath = MS_GRAPH_JSON_PATH
scopes = ['User.Read']
# port configurations
API_PORT = 9501
# API_HOST = '192.168.1.33'
API_HOST = '0.0.0.0'
# configure file all file paths
API_KEYS_FILE = api_key_file_path
LOG_FILE_PATH = log_file_path
INTENTS_FILE_PATH = intents_file_path
TEMPLATE_FOLDER_PATH = template_folder_path

# url of lang tool python server api
URL_OF_LANG_TOOL_PYTHON = 'https://api.languagetool.org/v2/check'

# prompt to get answer from the chatbot for specific question
PROMPT = '''please answer the following question in a conversational tone with the user. Start with a direct and concise answer. Do not give the answer in too much detail; give answer shortly in 2-3 lines only. If the answer is not related to the following topics: ("llc-publication", "certified-copy", "certificate-of-good-standing", "amendments", "merger-acquisitions", "reinstatement-of-entity", "Registered Agent", "Independent Director", "Entity Monitoring", "Attorneys", "Beneficial Ownership Information","BOI" "Tax ID EIN", "C-Corp", "S-Corp", "LLC", "LP", "PC or PLLC", "DBA Registration", "Name Availability", "Conversation", "Corporate Kit and Seal", "Formation of Nonprofit - 501c3", "Application For Exemption", "State Tax Exemption", "Foreign State Registration", "UCC Filings", "Dissolution", "Merchpay"),and also if question is related to any finantial related then respond with: "Sorry for the inconvenience. We are not able to provide you an answer for your query. For further assistance, Please contact our support team at 866-638-3309." In this case, set the key as "None". Ensure the response strictly follows the structure {{"ans": "ans"}}; ans should not contain too many lines; it should only be 2-3 lines.
Question: {question}
Response structure: {{"ans": "ans"}}'''

PROMPT_TO_GET_JSON_DATA_FROM_ENTITY_FORMATION_INFO = '''Read below information_data and extract the specific data from the provided information_data in following json format where information_data = {data} and json_format is {json_format} dont miss any key from the json and dont mention any comments give exact structure as mention and if any of the field is missing in the {data} then return as invalid if not able to extract the values for key then take value as None'''

JSON_FORMAT = '''{
	"ENTITY NAME":"entity_name",
	"DOCUMENT TYPE":"document_type",
	"ENTITY TYPE":"entity_type",
	"DOS ID":"dos_id",
	"FILE DATE":"file_date",
	"FILE NUMBER":"file_number",
	"TRANSACTION NUMBER":"transaction_number",
	"EXISTENCE DATE":"existence_date",
	"DURATION/DISSOLUTION":"duration_dissolution",
	"COUNTY ":"county",
	"SERVICE OF PROCESS ADDRESS":"service_of_process_address",
	"EMAIL":"email",
	"FILLED_BY":"filed_by",
	"FILLER_ADDRESS":"filler_address",
	"SIGNATURE":"signaturer name only",
	"ROLE":"role",
	"STATE":"state"
}'''

# contact us message
UNRECOGNIZED_MSG = "Sorry for the inconvenience. We are not able to provide you answer for your query. For further assistence, Please contact our support team at 866-638-3309"

# all used regular expressions
CORPORATION_REGEX = r'(?<!\S)((s|c)[ -]?corp(?:oration)?)\b'
EMAIL_PATTERN = r"^(?!.*\.\.)([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,})$"
CONTACT_PATTERN = r"^\d{10}$"
NAME_PATTERN = "^[A-Za-z\s]+$"

# payment related keywords which used to block the ans related payment
FINANTIAL_KEYWORDS = ["Payment", "Financial", "Cost", "Price", "Fee", "Charges", "Bill", "Invoice", "Budget", "Rate",
                      "Discount", "Refund", "Deposit", "Credit", "Finance", "Expense", "Payable", "Receivable", "Loan",
                      "Mortgage", "Investment", "Funding", "Tax", "Revenue", "Salary", "Wage", "Earnings", "Income",
                      "Remuneration", "Compensation", "Payment plan", "Subscription", "Installment", "Down payment",
                      "pays", "pay"]

# words which should not be change at the time of spelling correction
PRESERVED_TERMS = ["pllc", "llc", "dba", "vstate"]

UNRECOGNIZED_INFO = 'sorry'

NOT_NULL_ERROR = '{string} should not be null'
NOT_FOUND = "data not found"
PAGE_NOT_FOUND = "page not found"
INVALID_NAME = "Invalid or missing name. Name is required."
INVALID_EMAIL = "Invalid Email"
INVALID_CONTACT = "Invalid or missing contact number"
INVALID_CONTACT_DETAILS = "please provide name ,email and contact number"

# java api constants
BASE_URL = "http://64.202.187.199:8765/decrypt"
# LEADS_API_ENDPOINT = "/contact/api/hubspot/saveLeads"
LEADS_API_ENDPOINT = "/contact/api/hubspot/saveLeads/{id}"
SIGN_IN_ENDPOINT = "/authentication/api/user/signin"
CONTACT_API_ENDPOINT = "/contact/api/contactDetails/getByUserId/{id}"
SAVE_METHOD = 'post'
GET_METHOD = 'get'

SIGN_IN_PAYLOAD = {
        "username": "santosh@redberyltech.com",
        "password": "Santosh@123",
        "latDetails": "sadadasd",
        "longDetails": "asdasd",
        "ipAddress": "asadad"
}

PAYLOAD = {
        "properties": {
            "hs_lead_name": None,
            "first_name": None,
            "last_name": None,
            "company_name": None,
            "county": None,
            "email": None,
            "entity_type": None,
            "address": None,
            "message": None,
            "phone_number": None,
            "state": None,
            "zip_code": None
        },
        "associations": [
            {
                "types": [
                    {
                        "associationCategory": None,
                        "associationTypeId": None
                    }
                ],
                "to": {
                    "id": None
                }
            }
        ]
    }

 # ************************** image_extraction_for_identity_BOI******************************
CLASSIFICATION_PROMPT = """
Analyze this document image and identify the type of document by extracting only the following specific keywords if they are present: "license," "Pancard," or "aadharcard." , "passport," . Return the result in the following JSON format:        {
            "document_type": "The type of document (e.g., 'Pancard', 'License', 'AadhaarCard', etc.)",
            "confidence_score": "A score between 0 and 1 indicating confidence in classification",
            "document_features": ["List of key features identified that helped in classification"]
        }
        Be specific with the document type and ensure that the document is valid  and only classify if confident.
        """


AADHAR_CARD_EXTRACTION = """
        Extract the following fields from the Aadhaar card in JSON format:
        {
            "document_type": "AadhaarCard",
            "data": {
                "first_name": "",
                "last_name":"",
                "Email": "",
                "Phone": "",
                "date_of_birth": "",
                "Address": "",
                "city": "",
                "state": "",
                "country": "",
                "zip_code": "",
                "aadhaar_number": ""
            }
        }
        Ensure Aadhaar number is properly formatted and dates are in YYYY-MM-DD format.
        """
PAN_CARD_EXTRACTION = """
        Extract the following fields from the PAN card in JSON format:
        {
            "document_type": "PAN_Card",
            "data": {
                "first_name": "",
                "last_name":"",
                "Email": "",
                "Phone": "",
                "date_of_birth": "",
                "Address": "",
                "city": "",
                "state": "",
                "country": "",
                "zip_code": "",
                "pan_number": ""
            }
        }
        Ensure PAN number is in correct format (AAAPL1234C) and dates are in YYYY-MM-DD format.
        """
LICENSE_EXTRACTION = """
        Extract the following fields from the driving license in JSON format:
        {
            "document_type": "State Issued Driver_License",
            "data": {
                "first_name": "",
                "last_name":"",
                "Email": "",
                "Phone": "",
                "date_of_birth": "",
                "Address": "",
                "city": "",
                "state": "",
                "country": "",
                "zip_code": "",
                "license_number": ""
            }
        }
        Ensure all dates are in YYYY-MM-DD format and text fields are properly cased.
        """

PASSPORT_EXTRACTION =  """


Extract the following fields from the Passport in JSON format:
        {
            "document_type": "US Passport",
            "data": {
                "first_name": "",
                "last_name":"",
                "Email": "",
                "Phone": "",
                "date_of_birth": "",
                "Address": "",
                "city": "",
                "state": "",
                "country": "",
                "zip_code": "",
                "passport_number": ""
            }
        }
        Ensure passport number is in correct format (A1234567) and dates are in YYYY-MM-DD format.
        Type should be one of: P (Personal), D (Diplomatic), S (Service)
        Country code should be standard 3-letter code (e.g., IND for India)


"""
# **********************Offline form constants******************
OFFLINE_FORM_TEMPLATES_PATH = offline_form_templates
MAPPED_JSON_PROMPT = """
You are an intelligent assistant helping to fill out PDF forms using data provided in a user JSON.

Each form field is described by:
- `key`: the name of the field in the PDF.
- `text_near_key`: nearby labels or instructions from the PDF that provide context for the field's meaning.
- `placeholder`: the sample or default text currently inside the field, which can strongly indicate what kind of information is expected.

Your task is to:
1. Understand what each form field is requesting based on both `text_near_key` and especially the `placeholder`.
2. Use the mapping rules provided below to find the most appropriate value from the user JSON.
3. Return a JSON object that maps the PDF field `key` to the selected value from the user JSON.
4. Only include fields that have a confident match.

### FORM FIELD DESCRIPTIONS
{form_keys}

### USER JSON DATA
{user_json}

### PLACEHOLDER-TO-VALUE MAPPING RULES
The following mapping rules describe what value to take from the user JSON when a specific placeholder is found. Use these rules with high priority over other heuristics:

{mapping_rules}

### OUTPUT FORMAT
Return only a valid JSON dictionary like:
{{
  "PDF Field Key": "Mapped User Value",
  ...
}}

### NOTES
- Focus primarily on the `placeholder` value to infer the field's intent.
- Use nearby text only as supportive context.
- Be concise and accurate.
- If you are not confident in a match, do not include the field in the output.
"""

def _generate_mapping_rules():
    """
    Generates the mapping rules programmatically to improve maintainability.
    This function combines base entities with attributes to create a set of mapping rules.
    Special cases that do not fit the generation pattern are handled separately.
    """
    base_entities = {
        "RA": "Registered Agent",
        "Dr": "Director",
        "P": "Principal Address",
        "Inc": "Incorporator",
        "Mom": "Member or Manager",
        "MOM": "Member or Manager",
        "PA": "Principal Address",
    }

    attributes = {
        "zip": "Zip Code",
        "Zip": "Zip Code",
        "st": "State",
        "S": "State",
        "city": "City",
        "state": "State",
        "Address line 1": "street address",
        "Address line 2": "Address Line 2",
        "Address Zip Code": "Address Zip Code",
        "Mailing address": "Mailing Address",
    }

    generated_rules = {}

    for entity_abbr, entity_name in base_entities.items():
        for attr_abbr, attr_name in attributes.items():
            # Format with space
            generated_rules[f"{entity_abbr} {attr_abbr}"] = f"{entity_name} {attr_name}"
            # Format with space and lowercase attribute
            generated_rules[f"{entity_abbr} {attr_abbr.lower()}"] = f"{entity_name} {attr_name}"
            # Format with no space, capitalized attribute
            if not attr_abbr.islower():
                generated_rules[f"{entity_abbr}{attr_abbr}"] = f"{entity_name} {attr_name}"
            # Format with no space, lowercase attribute
            generated_rules[f"{entity_abbr}{attr_abbr.lower()}"] = f"{entity_name} {attr_name}"


    special_cases = {
        "RAMAZ": "RA mailing Address zip code",
        "DS": "Director State",
        "RS": "Registered Agent state",
        "PS": "Principal Address state",
        "IS": "Incorporator State",
        "PZIP": "Principal Address Zip Code",
        "RA MailingAdd zip": "RA mailing Address zip code",
        "Entity Name": "Legal Name",
        # This one has "Register" instead of "Registered"
        "RA Zip": "Register Agent Zip Code",
        "RA Address city": "Registered Agent City"
    }
    
    generated_rules.update(special_cases)

    return generated_rules

mapping_rules = _generate_mapping_rules()



