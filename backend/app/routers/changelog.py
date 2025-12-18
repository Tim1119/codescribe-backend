from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
from app.services.claude_service import ClaudeService
from app.prompts.changelog_prompts import CHANGELOG_SYSTEM_PROMPT, get_changelog_prompt

router = APIRouter()
claude_service = ClaudeService()

class ChangelogRequest(BaseModel):
    old_code: str
    new_code: str
    format: str

class ChangelogResponse(BaseModel):
    changelog: str
    version_suggestion: str
    breaking_changes: List[str]

@router.post("/generate", response_model=ChangelogResponse)
async def generate_changelog(request: ChangelogRequest):
    try:
        user_prompt = get_changelog_prompt(request.old_code, request.new_code, request.format)
        response_text = await claude_service.generate(CHANGELOG_SYSTEM_PROMPT, user_prompt)
        
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return ChangelogResponse(**data)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return ChangelogResponse(
                changelog=response_text,
                version_suggestion="0.0.1",
                breaking_changes=[]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
