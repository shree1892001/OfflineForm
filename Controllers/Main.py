from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import warnings
import os
from Controllers.LoginController import router as auth_router
from Controllers.ChatBotController import router as bot_router
from Controllers.UpdateCompanyDetailsController import router as entity_router
from Controllers.LeadsController import router as leads_router
from Controllers.ImageExtractorController import router as identity_router
from pydantic import BaseModel
from Services.ChatBotService import ChatBotService
from Utils.ApplicationContext import app_context
from Services.GetOtpServiceOutlook import GetOtpServiceOutlook
from Constants.constant import API_HOST, API_PORT, MsGraphJsonPath
from Controllers.FillPdfController import router as fill_pdf_router


warnings.filterwarnings("ignore")

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    app.state.context = app_context.lemmatizer


@app.on_event("startup")
async def warm_up():
    lemmatizer = app.state.context
    dummy_question = "Hello"
    ChatBotService().chat(dummy_question, "home", lemmatizer)


class EmailRequest(BaseModel):
    subject: str
    username: str
    password: str


@app.post("/get-email")
async def get_email(request: EmailRequest):
    print(request)
    outlook_client = GetOtpServiceOutlook(request.username, request.password)
    latest_email = outlook_client.list_emails_by_subject(request.subject)
    if latest_email:
        email_id = latest_email['id']
        verification_code = outlook_client.get_email_body(email_id)
        os.remove(MsGraphJsonPath)
        return verification_code
    else:
        os.remove(MsGraphJsonPath)
        return "No email found with the given subject."


app.include_router(auth_router, prefix="/auth")
app.include_router(bot_router, prefix="/bot")
app.include_router(entity_router, prefix="/multipart")
app.include_router(leads_router, prefix="/leads")
app.include_router(identity_router, prefix="/extract")
app.include_router(fill_pdf_router, prefix="/pdf")




if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
