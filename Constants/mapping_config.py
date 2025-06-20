# Mapping configuration for PDF form field mapping
# This file contains all the mapping rules that can be easily modified without touching the main code

# Base entities and their full names
BASE_ENTITIES = {
    "RA": "Registered Agent",
    "Dr": "Director", 
    "P": "Principal Address",
    "Inc": "Incorporator",
    "Mom": "Member or Manager",
    "MOM": "Member or Manager",
    "PA": "Principal Address",
}

# Common attributes and their full names
ATTRIBUTES = {
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

# Special cases that don't follow the standard pattern
SPECIAL_CASES = {
    "RAMAZ": "RA mailing Address zip code",
    "DS": "Director State",
    "RS": "Registered Agent state", 
    "PS": "Principal Address state",
    "IS": "Incorporator State",
    "PZIP": "Principal Address Zip Code",
    "RA MailingAdd zip": "RA mailing Address zip code",
    "Entity Name": "Legal Name",
    "RA Zip": "Register Agent Zip Code",
    "RA Address city": "Registered Agent City"
}

# Additional mapping patterns that can be easily added
ADDITIONAL_PATTERNS = {
    # Add any additional patterns here
    # "pattern": "mapped_value"
}

# Configuration for generating combinations
GENERATION_CONFIG = {
    "include_spaces": True,  # Generate patterns with spaces
    "include_no_spaces": True,  # Generate patterns without spaces
    "include_lowercase": True,  # Generate lowercase variations
    "include_capitalized": True,  # Generate capitalized variations
} 