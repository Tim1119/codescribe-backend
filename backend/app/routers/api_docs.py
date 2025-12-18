from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from app.services.claude_service import ClaudeService
from app.prompts.api_docs_prompts import API_DOCS_SYSTEM_PROMPT, get_api_docs_prompt

router = APIRouter()
claude_service = ClaudeService()

class ApiDocsRequest(BaseModel):
    code: str
    framework: str

class Endpoint(BaseModel):
    method: str
    path: str
    summary: str
    parameters: List[Dict[str, Any]] = []
    responses: Dict[str, str] = {}

class ApiDocsResponse(BaseModel):
    endpoints: List[Endpoint]
    documentation: str

@router.post("/generate", response_model=ApiDocsResponse)
async def generate_api_docs(request: ApiDocsRequest):
    try:
        user_prompt = get_api_docs_prompt(request.code, request.framework)
        response_text = await claude_service.generate(API_DOCS_SYSTEM_PROMPT, user_prompt)
        
        # Parse the JSON response from Claude
        # This is a bit fragile, in a real app we'd want more robust parsing or structured output
        try:
            # Find the JSON block
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return ApiDocsResponse(**data)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            # Fallback if parsing fails
            print(f"Error parsing JSON: {e}")
            return ApiDocsResponse(endpoints=[], documentation=response_text)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
