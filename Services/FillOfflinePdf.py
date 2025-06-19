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

    # 3. Use Gemini 1.5 Flash to generate field mapping
    def generate_data_dict_with_gemini(self, form_keys, user_json):
        api_keys = CallAiService().read_api_keys(API_KEYS_FILE)
        current_key_index = 0
        while current_key_index < len(api_keys):
            try:
                api_key = api_keys[current_key_index]
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                form_keys = json.dumps(form_keys, indent=2)
                user_json = json.dumps(user_json, indent=2)
                print("User JSon",user_json)
                prompt = MAPPED_JSON_PROMPT.format(
                    form_keys=form_keys,
                    user_json=user_json, 
                    mapping_rules=json.dumps(mapping_rules, indent=2)
                )
                response = model.generate_content(prompt)
                text = response.text
                try:
                    start = text.find('{')
                    end = text.rfind('}') + 1
                    print(json.loads(text[start:end]))
                    return json.loads(text[start:end])
                except Exception as e:
                    print("Error parsing Gemini response:", e)
                    print("Raw response:\n", text)
                    return {}
            except Exception as e:
                logger.log_aspect('Error', f"An error occurred with API key {api_key}: {e}")
                CallAiService.remove_api_key(api_key, api_keys)
                current_key_index += 1

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

