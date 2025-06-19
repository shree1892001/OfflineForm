from fastapi import APIRouter
from pydantic import BaseModel
from Services.LoginService import LoginService
from Logging_file.logging_file import custom_logger

router = APIRouter()


class Form(BaseModel):
    input_data: str


@router.post("/login/")
@custom_logger.log_around
async def login(form: Form):
    return LoginService().login_to_chatbot(form)
