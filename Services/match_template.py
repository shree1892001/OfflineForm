import os
from pdf2image import convert_from_bytes
import pytesseract
from fuzzywuzzy import fuzz
from Constants.constant import TEMPLATE_FOLDER_PATH


class MatchTemplate:
    # ==============================
    # 1. Convert PDF to Image
    # ==============================
    def pdf_to_image(self, pdf_bytes):
        images = convert_from_bytes(pdf_bytes)
        return images[0]  # Use first page of the document

    # ==============================
    # 2. Extract Text using OCR
    # ==============================
    def extract_text(self, image):
        return pytesseract.image_to_string(image).strip().lower()

    def get_matched_template_score(self, file_bytes, state):
        try:
            # Get all matching PDF files containing the state name
            pdf_files = [file for file in os.listdir(TEMPLATE_FOLDER_PATH) if file.lower().endswith(".pdf")]
            matching_pdfs = [file for file in pdf_files if state.lower() in file.lower()]

            if not matching_pdfs:
                return {"error": f"No template found for state '{state}'!"}

            # Convert uploaded PDF to image
            uploaded_image = self.pdf_to_image(file_bytes)
            uploaded_text = self.extract_text(uploaded_image)

            best_match = None
            highest_similarity = 0

            for pdf_file in matching_pdfs:
                state_template_path = os.path.join(TEMPLATE_FOLDER_PATH, pdf_file)

                # Convert template PDF to image
                with open(state_template_path, "rb") as template_file:
                    template_bytes = template_file.read()
                    template_image = self.pdf_to_image(template_bytes)

                # Extract text from template
                template_text = self.extract_text(template_image)

                # Compute similarity
                text_similarity = fuzz.ratio(uploaded_text, template_text)

                # Track the best match
                if text_similarity > highest_similarity:
                    highest_similarity = text_similarity
                    best_match = {
                        "state": state,
                        "template": pdf_file,
                        "text_similarity": text_similarity,
                        "match": text_similarity >= 70,  # Set threshold at 70%
                        "message": True if text_similarity >= 70 else False
                    }
            print(best_match)
            return best_match if best_match else {"error": "No matching template found with a high enough similarity score."}

        except Exception as e:
            return {"error": str(e)}
