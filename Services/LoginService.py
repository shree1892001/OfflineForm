import re
from Constants.constant import *
from fastapi import HTTPException
from Exceptions.ExceptionHandling import ExceptionHandling


class LoginService:
    def login_to_chatbot(self, form):
        input_data = form.input_data.strip()
        if not input_data:
            raise HTTPException(status_code=500, detail=INVALID_CONTACT_DETAILS)
        else:
            # Split the input data by comma and trim spaces
            data_parts = [part.strip() for part in input_data.split(",")]

            name, email, contact = data_parts
            if email.lower() == "null" or not email:
                email = None
            if name.lower() == "null" or not name:
                name = None
            # Validate patterns for each field
            email_pattern = re.compile(EMAIL_PATTERN)
            contact_pattern = re.compile(CONTACT_PATTERN)

            if not name:
                raise HTTPException(status_code=500, detail=INVALID_NAME)
            if not contact_pattern.match(contact):
                raise HTTPException(status_code=500, detail=INVALID_CONTACT)
            if email and not email_pattern.match(email):
                raise HTTPException(status_code=500, detail=INVALID_EMAIL)

            # Prepare the response
            response_content = {"message": f"Name: {name}, Email: {email}, Contact: {contact}"}
            status = ExceptionHandling().success(response_content)
            return status
