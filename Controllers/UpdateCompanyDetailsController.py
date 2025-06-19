from fastapi import APIRouter, File, UploadFile, Form
from Services.UpdateCompanyDetails import UpdateCompanyDetails
from fastapi.responses import JSONResponse
from Services.match_template import MatchTemplate
from Logging_file.logging_file import custom_logger

router = APIRouter()


class StateName:
    def __init__(self, state: str):
        self.state = state


def error_response(message="Data not added"):
    """Reusable function for returning a 500 error response."""
    return JSONResponse(
        status_code=500,
        content={"detail": message}
    )


@router.post("/extract_form_data")
@custom_logger.log_around
async def update_company(state: str = Form(...), file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        # Check if file extension is valid
        if not file.filename.lower().endswith((".pdf", ".docx")):
            return error_response("Invalid file format. Only PDF and DOCX are allowed.")

        # Match template
        matched_result = MatchTemplate().get_matched_template_score(file_content, state)

        if not matched_result.get("match"):
            return error_response("Template matching failed.")

        # Update company details
        response = UpdateCompanyDetails().update_company_details(file_content, file)
        if response == "Not Found":
            return error_response("Data not added")

        return response

    except Exception as e:
        return error_response(str(e))