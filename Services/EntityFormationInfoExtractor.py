from Services.FileDataExtractorService import FileProcessorFactory, ImageFileExtractorService, ScannedPDFPRocesser
from Constants.constant import PROMPT_TO_GET_JSON_DATA_FROM_ENTITY_FORMATION_INFO, JSON_FORMAT
import os, json, re
from Services.CallAiService import CallAiService
from Services.CleanDataService import CleanDataService
from Logging_file.logging_file import custom_logger

logger = custom_logger


class EntityFormationInfoExtractor:
    @custom_logger.log_around
    def get_json_of_entity_formation(self, file, file_name):
        try:
            data = FileProcessorFactory.get_processor(file,file_name)
            if data == "Unsupported file format":
                return "Not Found"
            image_data = ImageFileExtractorService().extract_text_from_images(file)
            combined_data = EntityFormationInfoExtractor().combine_text(data, image_data)
            json_data = self.get_clean_ai_response(combined_data)
            if json_data['ENTITY NAME'] == None:
                res = ScannedPDFPRocesser().get_scan_pdf_data(file, file_name)
                json_data = self.get_clean_ai_response(res)
                return json_data
            return json_data
        except Exception as e:
            logger.log_info(f"Error occured during get json data from the entity formation:: {str(e)}")
            return (str(e))

    def combine_text(self, pdf_text, image_text):
        combined_text = pdf_text + "\n\n" + image_text
        return combined_text

    def get_clean_ai_response(self,combined_data):
        ai_response = CallAiService().ai_api_call(
            PROMPT_TO_GET_JSON_DATA_FROM_ENTITY_FORMATION_INFO.format(data=combined_data, json_format=JSON_FORMAT))
        pattern = re.compile(r'\{(.*)\}', re.DOTALL)
        match = pattern.search(ai_response)
        if match:
            ai_response = '{' + match.group(1) + '}'
        ai_data = json.loads(ai_response)
        clean_ai_response = CleanDataService().clean_data(ai_data)
        cleaned_json = json.dumps(clean_ai_response, indent=4)
        json_data = json.loads(cleaned_json)
        return json_data
