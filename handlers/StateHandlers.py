# import os
# import json
# import pdfplumber
# import pytesseract
# from pdf2image import convert_from_path
# from docx import Document
# from Logging_file.logging_file import custom_logger
#
# logger = custom_logger
#
#
# def extract_pdf_format(pdf_path):
#     """
#     Extract the format (field names) from a regular or scanned PDF file.
#     """
#     extracted_fields = set()
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 text = page.extract_text()
#                 if text:
#                     extracted_fields.update(text.split())
#                 else:
#                     images = convert_from_path(pdf_path)
#                     for image in images:
#                         text = pytesseract.image_to_string(image)
#                         extracted_fields.update(text.split())
#
#         logger.log_info(f"Extracted fields from PDF: {extracted_fields}")
#         return extracted_fields
#     except Exception as e:
#         logger.log_info(f"Error extracting format from PDF: {str(e)}")
#         return set()
#
#
# def extract_docx_format(docx_path):
#     """
#     Extract the format (field names) from a DOCX file.
#     """
#     extracted_fields = set()
#     try:
#         doc = Document(docx_path)
#         for para in doc.paragraphs:
#             extracted_fields.update(para.text.split())
#         logger.log_info(f"Extracted fields from DOCX: {extracted_fields}")
#         return extracted_fields
#     except Exception as e:
#         logger.log_info(f"Error extracting format from DOCX: {str(e)}")
#         return set()
#
#
# def sanitize_state_code(state_code):
#     """
#     Ensure the state code is always a valid string.
#     """
#     if isinstance(state_code, dict):
#         state_code = state_code.get("name", "Unknown")  # Adjust this based on actual key structure
#     if not isinstance(state_code, str):
#         logger.log_info(f"Invalid state code format: {state_code}")
#         return None
#     return state_code.strip().replace(" ", "_").lower()  # Normalize format
#
#
# def save_state_format(fields, state_code):
#     """
#     Save the format template for a specific state in a plain text format.
#     """
#     try:
#         state_code = sanitize_state_code(state_code)
#         if not state_code:
#             return False
#
#         formats_dir = "state_formats"
#         if not os.path.exists(formats_dir):
#             os.makedirs(formats_dir)
#
#         file_path = os.path.join(formats_dir, f"{state_code}_format.txt")
#         with open(file_path, 'w') as f:
#             f.write("\n".join(fields))  # Store as plain text
#
#         logger.log_info(f"Format for state {state_code} saved at {file_path}")
#         return True
#     except Exception as e:
#         logger.log_info(f"Error saving format template: {str(e)}")
#         return False
#
#
# def compare_with_state_format(data, state_code):
#     """
#     Compare the extracted data fields with the existing format template.
#
#     Parameters:
#     data: Either a file path (string) or a dictionary of already extracted fields
#     state_code: The state code to use for template comparison
#
#     Returns:
#     Dictionary with comparison results
#     """
#     try:
#         # Log the incoming parameters for debugging
#         logger.log_info(f"compare_with_state_format called with file_path: {data}, state_code: {state_code}")
#
#         # Process state code
#         state_code = sanitize_state_code(state_code)
#         if not state_code:
#             return {"error": "Invalid state code format"}
#
#         formats_dir = "state_formats"
#         file_path_format = os.path.join(formats_dir, f"{state_code}_format.txt")
#
#         # Determine if data is a file path or already extracted data
#         if isinstance(data, dict):
#             # Data is already a dictionary of extracted fields
#             logger.log_info(f"Input is a dictionary of extracted fields")
#             extracted_fields = set(data.keys())
#         elif isinstance(data, str):
#             # Data is a file path
#             logger.log_info(f"Input is a file path: {data}")
#             if data.lower().endswith(".pdf"):
#                 extracted_fields = extract_pdf_format(data)
#             elif data.lower().endswith(".docx"):
#                 extracted_fields = extract_docx_format(data)
#             else:
#                 logger.log_info(f"Unsupported file format: {data}")
#                 return {"error": f"Unsupported file format: {data}"}
#         else:
#             logger.log_info(f"Invalid input type: {type(data)}")
#             return {"error": f"Invalid input type: {type(data)}"}
#
#         # Create a new template if one doesn't exist
#         if not os.path.exists(file_path_format):
#             logger.log_info(f"No existing template for {state_code}. Creating new template.")
#             save_state_format(extracted_fields, state_code)
#             return {"is_matching": True, "is_new_template": True, "missing_fields": [], "extra_fields": []}
#
#         # Load the existing template (as plain text)
#         with open(file_path_format, 'r') as f:
#             template_fields = set(f.read().splitlines())
#
#         missing_fields = template_fields - extracted_fields
#         extra_fields = extracted_fields - template_fields
#
#         is_valid = len(missing_fields) == 0
#         logger.log_info(
#             f"Validation result for {state_code}: Valid={is_valid}, Missing={list(missing_fields)}, Extra={list(extra_fields)}")
#
#         return {
#             "is_matching": is_valid,
#             "is_new_template": False,
#             "missing_fields": list(missing_fields),
#             "extra_fields": list(extra_fields)
#         }
#     except Exception as e:
#         logger.log_info(f"Error in format comparison: {str(e)}")
#         return {"error": str(e)}

import os
import json
from Logging_file.logging_file import custom_logger

logger = custom_logger


def sanitize_state_code(state_code):
    """
    Ensure the state code is always a valid string.
    """
    if isinstance(state_code, dict):
        state_code = state_code.get("name", "Unknown")  # Adjust this based on actual key structure
    if not isinstance(state_code, str):
        logger.log_info(f"Invalid state code format: {state_code}")
        return None
    return state_code.strip().replace(" ", "_").lower()  # Normalize format


def save_state_format(fields, state_code):
    """
    Save the format template for a specific state in a plain text format.

    Args:
        fields: Set or list of field names to save as template
        state_code: State code to identify the template

    Returns:
        Boolean indicating success or failure
    """
    try:
        state_code = sanitize_state_code(state_code)
        if not state_code:
            return False

        formats_dir = "state_formats"
        if not os.path.exists(formats_dir):
            os.makedirs(formats_dir)

        file_path = os.path.join(formats_dir, f"{state_code}_format.txt")
        with open(file_path, 'w') as f:
            f.write("\n".join(fields))  # Store as plain text

        logger.log_info(f"Format for state {state_code} saved at {file_path}")
        return True
    except Exception as e:
        logger.log_info(f"Error saving format template: {str(e)}")
        return False


def get_state_template(state_code):
    """
    Retrieve the existing format template for a specific state.

    Args:
        state_code: State code to identify which template to retrieve

    Returns:
        Dictionary containing:
            - success: Boolean indicating whether retrieval was successful
            - fields: List of template fields (if template exists)
            - error: Error message (if applicable)
    """
    try:
        # Sanitize state code
        state_code = sanitize_state_code(state_code)
        if not state_code:
            logger.log_info("Invalid state code provided to get_state_template")
            return {
                "success": False,
                "fields": [],
                "error": "Invalid state code format"
            }

        # Check if template exists
        formats_dir = "state_formats"
        file_path_format = os.path.join(formats_dir, f"{state_code}_format.txt")

        if not os.path.exists(file_path_format):
            logger.log_info(f"No existing template found for state code: {state_code}")
            return {
                "success": False,
                "fields": [],
                "error": f"No template exists for state: {state_code}"
            }

        # Load the existing template
        with open(file_path_format, 'r') as f:
            template_fields = f.read().splitlines()

        logger.log_info(f"Successfully retrieved template for {state_code} with {len(template_fields)} fields")

        return {
            "success": True,
            "fields": template_fields,
            "error": None
        }

    except Exception as e:
        error_msg = f"Error retrieving state template: {str(e)}"
        logger.log_info(error_msg)
        return {
            "success": False,
            "fields": [],
            "error": error_msg
        }
def compare_with_state_format(extracted_data, state_code):
    """
    Compare extracted data fields with the existing format template.

    Args:
        extracted_data: Dictionary containing extracted fields from document
        state_code: State code to identify which template to compare against

    Returns:
        Dictionary with comparison results including matching status and missing fields
    """
    try:
        logger.log_info(
            f"compare_with_state_format called with extracted_data keys: {list(extracted_data.keys())}, state_code: {state_code}")

        # Verify document state matches the provided state code
        document_state = extracted_data.get('STATE')
        if document_state:
            if not state_code.strip().lower() == document_state.strip().lower():
                logger.log_info(
                    f"State mismatch: Provided state '{state_code}' doesn't match document state '{document_state}'")
                return {
                    "error": f"State mismatch: Document is from {document_state}, but was validated against {state_code}",
                    "is_matching": False
                }

        # Process state code
        state_code = sanitize_state_code(state_code)
        if not state_code:
            return {"error": "Invalid state code format"}

        # Get field names from the extracted data
        if not isinstance(extracted_data, dict):
            logger.log_info(f"Invalid extracted_data format: {type(extracted_data)}")
            return {"error": f"Invalid extracted_data format: expected dictionary, got {type(extracted_data)}"}

        extracted_fields = set(extracted_data.keys())
        logger.log_info(f"Extracted fields: {extracted_fields}")

        # Check if template exists
        formats_dir = "state_formats"
        file_path_format = os.path.join(formats_dir, f"{state_code}_format.txt")

        if not os.path.exists(file_path_format):
            logger.log_info(f"No existing template for {state_code}. Creating new template.")
            save_state_format(extracted_fields, state_code)
            return {
                "is_matching": True,
                "is_new_template": True,
                "missing_fields": [],
                "extra_fields": []
            }

        # Load the existing template
        with open(file_path_format, 'r') as f:
            template_fields = set(f.read().splitlines())

        logger.log_info(f"Template fields for {state_code}: {template_fields}")

        # Compare fields
        missing_fields = template_fields - extracted_fields
        extra_fields = extracted_fields - template_fields

        is_valid = len(missing_fields) == 0
        logger.log_info(
            f"Validation result for {state_code}: Valid={is_valid}, Missing={list(missing_fields)}, Extra={list(extra_fields)}")

        return {
            "is_matching": is_valid,
            "is_new_template": False,
            "missing_fields": list(missing_fields),
            "extra_fields": list(extra_fields)
        }
    except Exception as e:
        logger.log_info(f"Error in format comparison: {str(e)}")
        return {"error": str(e)}