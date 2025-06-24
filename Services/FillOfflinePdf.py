import json
from io import BytesIO
from pdfrw import PdfReader, PdfName, PdfString, PdfWriter
from pdf2image import convert_from_path
import pytesseract
import tempfile
import fitz
import codecs
from Services.CallAiService import *

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = PdfName('V')
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


class FillOfflinePdf:
    def extract_ocr_lines_per_page(self, pdf_path):
        temp_dir = tempfile.mkdtemp()
        images = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir)
        ocr_data_per_page = []

        for image in images:
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            page_lines = []

            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                if text:
                    x, y = ocr_data['left'][i], ocr_data['top'][i]
                    w, h = ocr_data['width'][i], ocr_data['height'][i]
                    bbox = (x, y, x + w, y + h)
                    page_lines.append((text, bbox))

            ocr_data_per_page.append(page_lines)
        return ocr_data_per_page

    def extract_pdf_keys(self, input_pdf_path):
        doc = fitz.open(input_pdf_path)
        field_data = []
        ocr_lines_per_page = self.extract_ocr_lines_per_page(input_pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            widgets = page.widgets()
            for widget in widgets:
                if widget.field_name:
                    key = widget.field_name.strip()
                    rect = widget.rect  # field location on PDF in points
                    scale = 300 / 72
                    field_top = rect.y0 * scale
                    field_left = rect.x0 * scale
                    # OCR lines on this page
                    ocr_lines = ocr_lines_per_page[page_num]
                    nearby_text = []

                    for text, (x0, y0, x1, y1) in ocr_lines:
                        # Condition: line is above or very near to the form field
                        vertical_distance = field_top - y1
                        horizontal_overlap = abs(field_left - x0) < 200
                        if 0 < vertical_distance < 100 and horizontal_overlap:
                            nearby_text.append(text)

                    field_data.append({
                        'key': key,
                        'text_near_key': nearby_text[-2:],
                        'placeholder': widget.field_value
                    })

        print("✅ Final extracted data:")
        for item in field_data:
            print(item)

        return field_data

    # Primary method using database mappings with original JSON, AI as fallback
    def generate_data_dict_with_ai_mapping(self, form_keys, user_json):
        """
        Primary method using database mappings with original JSON, AI as fallback
        """
        # Keep the original user JSON as-is - no transformation needed
        original_user_json = user_json
        
        print("✅ Using original user JSON with database mappings")
        print("Original data:", json.dumps(original_user_json, indent=2))

        # Try database mapping first
        try:
            from Utils.capitalized_json_mapper import CapitalizedJsonMapper
            import yaml
            
            # Load configuration
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            # Initialize capitalized mapper
            mapper = CapitalizedJsonMapper(config)
            mapper.initialize_capitalized_mappings()
            
            # Get database mappings
            db_mappings = mapper.db_service.get_all_json_mappings()
            
            # Create result dictionary for PDF fields
            result = {}
            
            # First, ensure all PDF form fields are present
            for field in form_keys:
                field_name = field.get('key', '')
                if field_name:
                    result[field_name] = ""
            
            # Apply database mappings to map PDF fields to original user JSON
            mappings_applied = 0
            
            # Extract payload from the nested JSON structure first
            from Utils.mapping_utils import generate_mapping_rules, initialize_database_with_default_data
            mapper_temp = CapitalizedJsonMapper(config)
            extracted_payload = mapper_temp.extract_payload_from_source(original_user_json)
            
            print(f"Extracted payload for database mapping: {json.dumps(extracted_payload, indent=2)}")
            
            # Get mapping rules from mapping_utils.py (includes special cases)
            try:
                # Initialize database with default data (includes special cases)
                initialize_database_with_default_data(config)
                
                # Get mapping rules
                mapping_rules = generate_mapping_rules(config)
                
                print(f"Loaded mapping rules with special cases: {len(mapping_rules)} rules")
                
                # Apply special cases and mapping rules
                for field in form_keys:
                    pdf_field_name = field.get('key', '')
                    if not pdf_field_name:
                        continue
                    
                    # Check if this PDF field is in the mapping rules (flat structure)
                    if pdf_field_name in mapping_rules:
                        special_case_target = mapping_rules[pdf_field_name]
                        print(f"Found mapping rule: '{pdf_field_name}' -> '{special_case_target}'")
                        
                        # Map the special case to the appropriate data source
                        user_value = None  # Initialize user_value
                        if 'Legal Name' in special_case_target:
                            user_value = mapper_temp._get_value_by_path(extracted_payload, "name.legal_name")
                        elif 'Registered Agent' in special_case_target:
                            if 'City' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.city")
                            elif 'State' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.state")
                            elif 'Zip Code' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.zip_code")
                            elif 'Name' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.keyPersonnelName")
                            elif 'Mailing Information Zip Code' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.zip_code")
                            elif 'Mailing Information State' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.state")
                        elif 'Principal Address' in special_case_target:
                            if 'City' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.city")
                            elif 'State' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.state")
                            elif 'Zip Code' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.zip_code")
                        elif 'Director' in special_case_target:
                            if 'State' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.state")
                        elif 'Incorporator' in special_case_target:
                            if 'State' in special_case_target:
                                user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.state")
                        
                        if user_value is not None:
                            result[pdf_field_name] = user_value
                            mappings_applied += 1
                            print(f"Mapping rule applied: PDF '{pdf_field_name}' -> '{special_case_target}': {user_value}")
                    
                    # Also check for base entity patterns in the field name
                    else:
                        # Check if field name contains entity patterns
                        entity_patterns = {
                            'RA': 'Registered Agent',
                            'PA': 'Principal Address',
                            'Dr': 'Director',
                            'Inc': 'Incorporator',
                            'Mom': 'Member or Manager',
                            'MOM': 'Member or Manager'
                        }
                        
                        user_value = None  # Initialize user_value for entity patterns
                        for pattern, entity_name in entity_patterns.items():
                            if pattern in pdf_field_name:
                                # Map based on entity type and field type
                                if entity_name == "Registered Agent":
                                    if "city" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.city")
                                    elif "state" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.state")
                                    elif "zip" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.Address.zip_code")
                                    elif "name" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.keyPersonnelName")
                                    elif "email" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.emailId")
                                    elif "contact" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "Registered_Agent.contactNo")
                                elif entity_name == "Principal Address":
                                    if "city" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.city")
                                    elif "state" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.state")
                                    elif "zip" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.zip_code")
                                    elif "address" in pdf_field_name.lower():
                                        user_value = mapper_temp._get_value_by_path(extracted_payload, "principal_address.street_address")
                                
                                if user_value is not None:
                                    result[pdf_field_name] = user_value
                                    mappings_applied += 1
                                    print(f"Entity pattern mapping: PDF '{pdf_field_name}' -> '{entity_name}': {user_value}")
                                    break
                
                # Also apply database JSON mappings for additional coverage
                for db_mapping in db_mappings:
                    pdf_field_name = db_mapping.target_path
                    user_field_path = db_mapping.source_path
                    relative_path = user_field_path.replace("payload.", "")
                    
                    # Check if this PDF field exists in our form keys and hasn't been mapped yet
                    if any(field.get('key') == pdf_field_name for field in form_keys) and not result.get(pdf_field_name):
                        user_value = mapper_temp._get_value_by_path(extracted_payload, relative_path)
                        
                        if user_value is not None:
                            result[pdf_field_name] = user_value
                            mappings_applied += 1
                            print(f"Database JSON mapping: PDF '{pdf_field_name}' -> '{relative_path}': {user_value}")
                
            except Exception as e:
                print(f"Error applying mapping rules: {e}")
                # Fallback to basic database mappings
                for db_mapping in db_mappings:
                    pdf_field_name = db_mapping.target_path
                    user_field_path = db_mapping.source_path
                    relative_path = user_field_path.replace("payload.", "")
                    
                    if any(field.get('key') == pdf_field_name for field in form_keys):
                        user_value = mapper_temp._get_value_by_path(extracted_payload, relative_path)
                        
                        if user_value is not None:
                            result[pdf_field_name] = user_value
                            mappings_applied += 1
                            print(f"Fallback database mapping: PDF '{pdf_field_name}' -> '{relative_path}': {user_value}")
            
            print(f"✅ Database mapping completed successfully")
            print(f"Mapped {mappings_applied} fields out of {len(result)} total PDF fields using database")
            
            # Check if we have enough mappings, if not, use AI fallback
            mapped_fields = len([v for v in result.values() if v])
            if mapped_fields < len(result) * 0.3:  # If less than 30% mapped, use AI
                print(f"⚠️ Only {mapped_fields}/{len(result)} fields mapped by database, using AI fallback...")
                return self._use_ai_fallback(form_keys, original_user_json, result)
            
            return result
            
        except Exception as e:
            print(f"❌ Error in database mapping: {e}")
            print("🔄 Falling back to AI mapping...")
            return self._use_ai_fallback(form_keys, original_user_json, {})

    def _use_ai_fallback(self, form_keys, original_user_json, existing_result):
        """Use AI as fallback when database mapping is insufficient"""
        api_keys = CallAiService().read_api_keys(API_KEYS_FILE)
        current_key_index = 0
        while current_key_index < len(api_keys):
            try:
                api_key = api_keys[current_key_index]
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                form_keys_json = json.dumps(form_keys, indent=2)
                payload_json_str = json.dumps(original_user_json, indent=2)
                print("Original User JSON (for AI fallback):", payload_json_str)
                
                # AI prompt for field mapping - map PDF fields to original JSON keys
                prompt = f"""
You are an expert JSON field mapper for PDF form filling. Your task is to map PDF form fields to user data in the original JSON structure.

**CONTEXT:**
- You have a list of PDF form fields extracted from a PDF template
- You have user data in the original JSON format (untouched/not transformed)
- You need to create a mapping dictionary where keys are PDF field names and values are extracted from the original user JSON

**PDF FORM FIELDS:**
{form_keys_json}

**ORIGINAL USER DATA (untouched):**
{payload_json_str}

**MAPPING RULES:**
1. **Exact Match Priority**: Look for exact field name matches first in the user JSON
2. **Semantic Matching**: Match PDF fields to user JSON fields based on meaning and context
3. **Nested Data Extraction**: Extract values from nested JSON structures in the user data
4. **Data Type Consistency**: Ensure data types match (string, number, etc.)
5. **Default Values**: Use empty string for missing data, not null

**COMMON MAPPING PATTERNS:**
- PDF "CD_Legal_Name", "CD_LLC_Name" → User JSON "legal_name", "entity_name", "company_name"
- PDF "PA_City", "RA_City" → User JSON "city", "address.city"
- PDF "Email", "Og_Email" → User JSON "emailId", "email", "contact.email"
- PDF "Contact_No", "Og_Contact_No" → User JSON "contactNo", "contact_number", "phone"

**SPECIAL MAPPING RULES:**
- If PDF has "CD_Legal_Name" or "CD_LLC_Name", look for "legal_name" in user JSON
- If PDF has "PA_City" or "RA_City", look for "city" in user JSON (check nested structures)
- If PDF has "Email" or "Og_Email", look for "emailId" or "email" in user JSON
- If PDF has "Contact_No" or "Og_Contact_No", look for "contactNo" or "contact_number" in user JSON
- Check both direct fields and nested structures (like "payload.name.legal_name")

**OUTPUT REQUIREMENTS:**
1. Return ONLY a valid JSON object
2. Keys should be PDF field names (exactly as provided)
3. Values should be extracted from the original user JSON
4. Do not include explanations or comments in the JSON
5. Handle missing data gracefully with empty strings
6. Ensure all PDF fields are included in the output

**EXAMPLE OUTPUT FORMAT:**
{{
    "PDF_Field_Name_1": "extracted_value_from_user_json_1",
    "PDF_Field_Name_2": "extracted_value_from_user_json_2",
    "PDF_Field_Name_3": ""
}}

**IMPORTANT:**
- Focus on the PDF field names provided in the form_keys
- Extract relevant data from the original user_json structure (don't transform it)
- If a field has no matching data, use empty string ""
- Ensure the output is valid JSON that can be parsed
- Apply semantic understanding to map similar fields
- Check nested structures like "payload.name.legal_name" for values

Now create the mapping dictionary by mapping PDF fields to original user JSON data:
"""
                
                response = model.generate_content(prompt)
                text = response.text
                try:
                    # Extract JSON from response
                    start = text.find('{')
                    end = text.rfind('}') + 1
                    
                    if start == -1 or end == 0:
                        print("❌ No JSON found in AI response")
                        return existing_result
                    
                    json_str = text[start:end]
                    ai_result = json.loads(json_str)
                    
                    # Validate the result
                    if not isinstance(ai_result, dict):
                        print("❌ AI response is not a dictionary")
                        return existing_result
                    
                    # Merge AI results with existing database results
                    for field in form_keys:
                        field_name = field.get('key', '')
                        if field_name:
                            if field_name not in existing_result or not existing_result[field_name]:
                                existing_result[field_name] = ai_result.get(field_name, "")
                    
                    print("✅ AI fallback mapping completed successfully")
                    print(f"AI mapped {len([v for v in ai_result.values() if v])} additional fields")
                    
                    return existing_result
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing AI JSON response: {e}")
                    print("Raw response:\n", text)
                    return existing_result
                except Exception as e:
                    print(f"❌ Unexpected error processing AI response: {e}")
                    print("Raw response:\n", text)
                    return existing_result
                    
            except Exception as e:
                logger.log_aspect('Error', f"An error occurred with API key {api_key}: {e}")
                CallAiService.remove_api_key(api_key, api_keys)
                current_key_index += 1
        
        print("❌ All API keys failed, returning existing database results")
        return existing_result

    def _flatten_payload_data(self, payload_data):
        """
        Flatten nested payload data for PDF filling
        """
        flattened = {}
        
        def flatten_recursive(data, prefix=""):
            for key, value in data.items():
                if isinstance(value, dict):
                    flatten_recursive(value, f"{prefix}{key}_" if prefix else f"{key}_")
                else:
                    field_key = f"{prefix}{key}" if prefix else key
                    if value is not None and value != "":
                        flattened[field_key] = value
        
        flatten_recursive(payload_data)
        return flattened

    def decode_key(self, raw_key):
        try:
            # Convert PdfString object to bytes if needed
            if hasattr(raw_key, 'decode'):
                raw_key = raw_key.decode()

            raw_str = str(raw_key)
            key_bytes = raw_str.encode('latin1')  # Preserve byte values

            # Check and decode UTF-16
            if key_bytes.startswith(codecs.BOM_UTF16_LE) or b'\x00' in key_bytes:
                return key_bytes.decode('utf-16').strip()

            return key_bytes.decode('latin1').strip()
        except Exception as e:
            print(f"Error decoding key: {raw_key} - {e}")
            return str(raw_key).strip()

    def fill_pdf(self, input_pdf_path, output_stream, data_dict):
        template_pdf = PdfReader(input_pdf_path)
        matched_keys = set()

        for page in template_pdf.pages:
            annotations = page.get(ANNOT_KEY)
            if not annotations:
                continue

            for annotation in annotations:
                if annotation.get(SUBTYPE_KEY) == WIDGET_SUBTYPE_KEY and annotation.get(ANNOT_FIELD_KEY):
                    raw_key = annotation[ANNOT_FIELD_KEY]
                    field_name = raw_key[1:-1].strip()

                    for key, value in data_dict.items():
                        if key in matched_keys:
                            continue  # Already filled this field

                        safe_value = "" if value is None else str(value)

                        # Direct match
                        if key == field_name:
                            annotation.update({PdfName('V'): PdfString.encode(safe_value)})
                            if '/AP' in annotation:
                                del annotation['/AP']
                            matched_keys.add(key)
                            print(f"✅ Field filled (direct): {key} -> {safe_value}")
                            break

                        # Partial/decoded match
                        elif key.endswith(self.decode_key(raw_key)):
                            annotation.update({PdfName('V'): PdfString.encode(safe_value)})
                            if '/AP' in annotation:
                                del annotation['/AP']
                            matched_keys.add(key)
                            print(f"✅ Field filled (partial): {key} -> {safe_value}")
                            break

        unmatched_list = [key for key in data_dict.keys() if key not in matched_keys]

        for key in unmatched_list:
            print(f"⚠️ Key '{key}' not found in PDF fields")

        PdfWriter().write(output_stream, template_pdf)
        output_stream.seek(0)
        return output_stream, unmatched_list

    def fill_pdf_with_random_data(self, input_pdf_stream, unmatched_list, data_dict):
        input_pdf_stream.seek(0)
        doc = fitz.open(stream=input_pdf_stream)

        for field_name in unmatched_list:
            value = data_dict.get(field_name, "")
            if not value:
                print(f"⚠️ No value found for unmatched field: {field_name}")
                continue

            filled = False
            for page in doc:
                widgets = page.widgets()
                for widget in widgets:
                    if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT and widget.field_name == field_name:
                        widget.field_value = value
                        widget.update()
                        print(f"✅ Field '{field_name}' filled with value: {value}")
                        filled = True
                        break
                if filled:
                    break
            if not filled:
                print(f"❌ Field '{field_name}' still not found in fitz document")

        # Save modified doc to a new BytesIO stream
        output_stream = BytesIO()
        doc.save(output_stream)
        return output_stream

