from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from Services.ChatBotService import ChatBotService
from fastapi.responses import JSONResponse

router = APIRouter()


class Question(BaseModel):
    page: str
    question: str


class Answer(BaseModel):
    answer: str


@router.post("/chat_with_us", response_model=Answer)
async def ask_question(request: Request, question: Question):
    try:
        lemmatizer = request.app.state.context
        response = ChatBotService().chat(question.question, question.page, lemmatizer)
        response_content = Answer(answer=response)
        return JSONResponse(content=response_content.dict(), status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
