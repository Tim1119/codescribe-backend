from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.claude_service import ClaudeService
from app.prompts.documentation_prompts import DOCUMENTATION_SYSTEM_PROMPT, get_documentation_prompt

router = APIRouter()
claude_service = ClaudeService()

class DocumentationRequest(BaseModel):
    code: str
    language: str
    style: str

class DocumentationResponse(BaseModel):
    documented_code: str
    summary: str

@router.post("/generate", response_model=DocumentationResponse)
async def generate_documentation(request: DocumentationRequest):
    try:
        user_prompt = get_documentation_prompt(request.code, request.language, request.style)
        documented_code = await claude_service.generate(DOCUMENTATION_SYSTEM_PROMPT, user_prompt)
        
        # Simple summary generation (could be enhanced)
        summary = "Documentation generated successfully."
        
        return DocumentationResponse(documented_code=documented_code, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
