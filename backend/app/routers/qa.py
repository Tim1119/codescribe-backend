from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from app.services.claude_service import ClaudeService
from app.prompts.qa_prompts import QA_SYSTEM_PROMPT, get_qa_prompt

router = APIRouter()
claude_service = ClaudeService()

class Message(BaseModel):
    role: str
    content: str

class QARequest(BaseModel):
    question: str
    code_context: str
    history: List[Message]

class CodeRef(BaseModel):
    file: str
    line_start: int
    line_end: int
    snippet: str

class QAResponse(BaseModel):
    answer: str
    code_references: List[CodeRef]

@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QARequest):
    try:
        # Convert Pydantic models to dicts for the prompt function
        history_dicts = [msg.dict() for msg in request.history]
        user_prompt = get_qa_prompt(request.question, request.code_context, history_dicts)
        response_text = await claude_service.generate(QA_SYSTEM_PROMPT, user_prompt)
        
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return QAResponse(**data)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return QAResponse(
                answer=response_text,
                code_references=[]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
