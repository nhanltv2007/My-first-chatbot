import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# Import chương trình
from Final_Model import respond

app = FastAPI(title = "Chat-NHA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/status', response_class=JSONResponse)
def root():
    return {"status": "Chat-NHA backend is running"}


class Question(BaseModel):
    question: str
@app.post("/ask")
def ask_question(data: Question):
    result = respond(data.question,1)
    return {
        "question":data.question,
        "answer": result[0]["answer"]
    }


class QA(BaseModel):
    question: str
    answer: str
@app.post("/add_qa")
def add_qa(data: QA):
    if os.path.exists("Static/Question_Library.json"):
        with open("Static/Question_Library.json", "r", encoding="utf-8") as f:
            qa = json.load(f)
    else:
        qa = {}

    qa[data.question] = data.answer

    with open("Static/Question_Library.json", "w", encoding="utf-8") as f:
        json.dump(qa, f, ensure_ascii=False, indent=2)
    return {"status": "ok"}



class SearchQuery(BaseModel):
    query: str
    k: int = 5
@app.post("/search")
def search_question(data: SearchQuery):
    results = respond(data.query, data.k)
    return results



class UpdateQA(BaseModel):
    old_question: str
    new_question: str
    new_answer: str
@app.post("/update_qa")
def update_qa(data: UpdateQA):
    with open("Static/Question_Library.json", "r", encoding="utf-8") as f:
        qa = json.load(f)

    # Xóa câu cũ
    qa.pop(data.old_question, None)

    # Thêm câu mới
    qa[data.new_question] = data.new_answer

    with open("Static/Question_Library.json", "w", encoding="utf-8") as f:
        json.dump(qa, f, ensure_ascii=False, indent=2)

    return {"status": "updated"}



# Kết nối trang html
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/questions", response_class=HTMLResponse)
def questions(request: Request):
    return templates.TemplateResponse(
        "Questions.html",
        {"request": request}
    )

@app.get("/add", response_class=HTMLResponse)
def add(request: Request):
    return templates.TemplateResponse(
        "Add_Question.html",
        {"request": request}
    )

@app.get("/fix", response_class=HTMLResponse)
def fix(request: Request):
    return templates.TemplateResponse(
        "Fix_Question.html",
        {"request": request}
    )
