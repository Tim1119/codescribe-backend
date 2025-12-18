from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
from app.services.claude_service import ClaudeService
from app.prompts.health_prompts import HEALTH_SYSTEM_PROMPT, get_health_prompt

router = APIRouter()
claude_service = ClaudeService()

class HealthRequest(BaseModel):
    code: str

class Suggestion(BaseModel):
    title: str
    description: str
    line: int

class ScoreBreakdown(BaseModel):
    completeness: int
    clarity: int
    accuracy: int
    coverage: int

class HealthResponse(BaseModel):
    score: int
    breakdown: ScoreBreakdown
    suggestions: List[Suggestion]

@router.get("/")
async def health_check():
    return {"status": "healthy"}

@router.post("/analyze", response_model=HealthResponse)
async def analyze_health(request: HealthRequest):
    try:
        user_prompt = get_health_prompt(request.code)
        response_text = await claude_service.generate(HEALTH_SYSTEM_PROMPT, user_prompt)
        
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return HealthResponse(**data)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            # Fallback
            return HealthResponse(
                score=0,
                breakdown=ScoreBreakdown(completeness=0, clarity=0, accuracy=0, coverage=0),
                suggestions=[Suggestion(title="Error", description="Failed to analyze code", line=0)]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
