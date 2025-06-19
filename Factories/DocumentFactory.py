from abc import ABC, abstractmethod
from typing import Dict, Any
import json
from Services.ImageExtractor import ImageTextExtractor
from Constants.constant import *
import re
import datetime


class DocumentExtractor(ABC):
    def __init__(self, api_key: str):
        self.image_extractor = ImageTextExtractor(api_key)

    @abstractmethod
    def get_extraction_prompt(self) -> str:
        """Return the specific prompt for this document type"""
        pass


    def extract_fields(self, image_path: str) -> Dict[str, Any]:
        """Extract fields using the document-specific prompt"""
        prompt = self.get_extraction_prompt()
        response = self.image_extractor.query_gemini_llm(image_path, prompt)
        clean_json = json.loads(response.strip().replace("```json", "").replace("```", "").strip())
        return clean_json


class LicenseExtractor(DocumentExtractor):
    def get_extraction_prompt(self) -> str:
        return LICENSE_EXTRACTION

    def validate_fields(self, extracted_data: Dict[str, Any]) -> bool:
        required_fields = {
            "license_number", "name", "date_of_birth",
            "valid_from", "valid_until"
        }
        return all(field in extracted_data.get("data", {}) for field in required_fields)


class PancardExtractor(DocumentExtractor):
    def get_extraction_prompt(self) -> str:
        return PAN_CARD_EXTRACTION
    def validate_fields(self, extracted_data: Dict[str, Any]) -> bool:
        required_fields = {"pan_number", "name", "fathers_name", "date_of_birth"}
        return all(field in extracted_data.get("data", {}) for field in required_fields)


class AadhaarCardExtractor(DocumentExtractor):
    def get_extraction_prompt(self) -> str:
        return AADHAR_CARD_EXTRACTION

    def validate_fields(self, extracted_data: Dict[str, Any]) -> bool:
        required_fields = {"aadhaar_number", "name", "gender", "date_of_birth"}
        return all(field in extracted_data.get("data", {}) for field in required_fields)



class PassportExtractor(DocumentExtractor):
    def get_extraction_prompt(self) -> str:
        return PASSPORT_EXTRACTION

    def validate_fields(self, extracted_data: Dict[str, Any]) -> bool:

        required_fields = {
            "passport_number",
            "first_name",
            "last_name",
            "Email",
            "Phone",
            "date_of_birth",
            "Address",
            "city",
            "state",
            "country",
            "zip_code"
        }

        if not all(field in extracted_data.get("data", {}) for field in required_fields):
            return False

        data = extracted_data.get("data", {})

        passport_number = data.get("passport_number", "")
        if not re.match(r'^[A-Z][0-9]{7}$', passport_number):
            return False

        date_fields = ["date_of_birth", "date_of_issue", "date_of_expiry"]
        for date_field in date_fields:
            date_value = data.get(date_field, "")
            try:
                datetime.strptime(date_value, '%Y-%m-%d')
            except ValueError:
                return False

        passport_type = data.get("type", "")
        if passport_type not in ["P", "D", "S"]:
            return False

        country_code = data.get("country_code", "")
        if not re.match(r'^[A-Z]{3}$', country_code):
            return False

        if data.get("gender", "").upper() not in ["M", "F", "X"]:
            return False

        return True
class DocumentExtractorFactory:
    _extractors = {
        "license": LicenseExtractor,
        "pan_card": PancardExtractor,
        "aadhaar_card": AadhaarCardExtractor,
        "aadhaarcard" : AadhaarCardExtractor,
        "Pancard": PancardExtractor,
        "pancard":PancardExtractor,
        "Passport" : PassportExtractor,
        "passport" : PassportExtractor
    }

    @classmethod
    def get_extractor(cls, document_type: str, api_key: str) -> DocumentExtractor:
        extractor_class = cls._extractors.get(document_type.lower().replace("_", ""))
        if not extractor_class:
            raise ValueError(f"No extractor found for document type: {document_type}")
        return extractor_class(api_key)

    @classmethod
    def register_extractor(cls, doc_type: str, extractor: type):
        if not issubclass(extractor, DocumentExtractor):
            raise ValueError("Extractor must inherit from DocumentExtractor")
        cls._extractors[doc_type.lower()] = extractor