from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Services.AddLeadsDataService import AddLeadsDetails
from fastapi.responses import JSONResponse
from typing import Optional
from Logging_file.logging_file import custom_logger

router = APIRouter()


class InputData(BaseModel):
    lead_name:Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    message: Optional[str] = None
    company_name: Optional[str] = None
    state: Optional[str] = None
    token: Optional[str] = None


@router.post("/add_leads_data")
@custom_logger.log_around
async def leads_data(form: InputData):
    try:
        response = AddLeadsDetails().add_leads_details(form.lead_name,form.first_name,form.last_name,form.email,form.phone_number,form.token,form.message,form.company_name,form.state)
        if response == 'Not Found':
            return JSONResponse(
                status_code=500,
                content={"detail": "Data not added"}
            )
        return JSONResponse(content="data added successfully", status_code=201)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Data not added"}
        )
