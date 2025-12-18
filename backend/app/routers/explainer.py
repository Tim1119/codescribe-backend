from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
from app.services.claude_service import ClaudeService
from app.prompts.explainer_prompts import EXPLAINER_SYSTEM_PROMPT, get_explainer_prompt

router = APIRouter()
claude_service = ClaudeService()

class ExplainerRequest(BaseModel):
    code: str
    level: str
    focus_area: Optional[str] = None

class ExplainerResponse(BaseModel):
    explanation: str
    key_concepts: List[str]
    analogies: List[str]

@router.post("/explain", response_model=ExplainerResponse)
async def explain_code(request: ExplainerRequest):
    try:
        user_prompt = get_explainer_prompt(request.code, request.level, request.focus_area)
        response_text = await claude_service.generate(EXPLAINER_SYSTEM_PROMPT, user_prompt)
        
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return ExplainerResponse(**data)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return ExplainerResponse(
                explanation=response_text,
                key_concepts=[],
                analogies=[]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
