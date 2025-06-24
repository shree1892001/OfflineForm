from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
import os, io, json, yaml
from Services.FillOfflinePdf import FillOfflinePdf as FormFiller
from Constants.constant import OFFLINE_FORM_TEMPLATES_PATH
from Logging_file.logging_file import custom_logger
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class Form_data(BaseModel):
    file_json_data: Dict[str, Any]

@router.post("/get_filled_pdf")
@custom_logger.log_around
async def process_form(file_json_data: str = Form(...)):
    try:
        parsed_data = json.loads(file_json_data)

        # Extract first item like Object.values(jsonData)[0]
        first_item = list(parsed_data.values())[0]

        state_name = first_item.get("State", {}).get("stateFullDesc")
        entity_name = first_item.get("EntityType", {}).get("orderShortName")

        if not state_name or not entity_name:
            return {"error": "Missing 'State.stateFullDesc' or 'EntityType.orderShortName'"}

        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        template_filename = f"{state_name}_{entity_name}".lower().replace(" ", "") + ".pdf"
        input_path = os.path.join(OFFLINE_FORM_TEMPLATES_PATH, template_filename)

        if not os.path.exists(input_path):
            return {"error": f"Template file not found: {input_path}"}

        form_filler = FormFiller()
        form_keys = form_filler.extract_pdf_keys(input_path)
        
        # Use the new database-driven mapping system
        mapped_data = form_filler.generate_data_dict_with_ai_mapping(form_keys, first_item)

        output_stream = io.BytesIO()
        output_stream, unmatched_list = form_filler.fill_pdf(input_path, output_stream, mapped_data)
        print("unmatched_list::", unmatched_list)

        final_output_stream = form_filler.fill_pdf_with_random_data(output_stream, unmatched_list, mapped_data)
        final_output_stream.seek(0)

        return StreamingResponse(
            content=final_output_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={state_name}_filled_form.pdf"}
        )

    except Exception as e:
        return {"error": str(e)}
