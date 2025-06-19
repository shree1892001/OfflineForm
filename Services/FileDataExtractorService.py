import docx2txt
from io import BytesIO
import fitz  # PyMuPDF
from pytesseract import image_to_string
from PIL import Image
import io, tempfile, ocrmypdf
from Logging_file.logging_file import custom_logger

logger = custom_logger


class PdfFileExtractorService:
    @custom_logger.log_around
    def pdf(self, file):
        try:
            pdf_text = ""
            if isinstance(file, bytes):
                file = io.BytesIO(file)

            doc = fitz.open(stream=file, filetype="pdf")
            for page in doc:
                pdf_text += page.get_text()

            doc.close()
            return pdf_text
        except Exception as e:
            logger.log_info("Error extracting data from PDF file", str(e))
            raise


class WordFileExtractorservice:
    @custom_logger.log_around
    def word(self, file):
        try:
            if isinstance(file, bytes):
                file = BytesIO(file)

            data = docx2txt.process(file)
            return data
        except Exception as e:
            logger.log_info("Error extracting data from Word file:", str(e))
            raise


class ImageFileExtractorService:
    def extract_text_from_images(self, file):
        try:
            file_stream = io.BytesIO(file)
            doc = fitz.open(stream=file_stream, filetype="pdf")

            image_text = ""
            for page in doc:
                for img_index, img in enumerate(page.get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = io.BytesIO(base_image["image"])
                    image = Image.open(image_bytes)
                    image_text += image_to_string(image) + "\n"

            doc.close()
            return image_text
        except Exception as e:
            return f"Error extracting text from images: {str(e)}"


class FileProcessorFactory:
    @staticmethod
    @custom_logger.log_around
    def get_processor(file,file_name):
        try:
            if file_name.filename.lower().endswith(".pdf"):
                return PdfFileExtractorService().pdf(file)
            elif file_name.filename.endswith(".docx"):
                return WordFileExtractorservice().word(file)
            else:
                raise ValueError(f"Unsupported file format")
        except Exception as e:
            logger.log_info(f"Error occurred due to file format processor :: {str(e)}")
            return str(e)

class ScannedPDFPRocesser:
    @staticmethod
    @custom_logger.log_around
    def get_scan_pdf_data(file,file_name):
        try:
            if file_name.filename.endswith(".pdf"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
                    temp_input.write(file)  # Write the bytes to temp file
                    temp_input_path = temp_input.name  # Get temp file path

                # Create a temporary output file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
                    temp_output_path = temp_output.name  # Get temp output file path

                # Apply OCR processing
                ocrmypdf.ocr(temp_input_path, temp_output_path, language="eng", force_ocr=True, deskew=True)
                with open(temp_output_path, "rb") as f:
                    processed_pdf_bytes = f.read()
                    res = FileProcessorFactory().get_processor(processed_pdf_bytes,file_name)
                    return res
            else:
                raise ValueError(f"Unsupported file format")
        except Exception as e:
            logger.log_info(f"Error occurred due to file format processor :: {str(e)}")
            return str(e)