from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.claude_service import ClaudeService
from app.prompts.readme_prompts import README_SYSTEM_PROMPT, get_readme_prompt

router = APIRouter()
claude_service = ClaudeService()

class FileContent(BaseModel):
    name: str
    content: str

class ReadmeRequest(BaseModel):
    files: List[FileContent]
    sections: List[str]
    template: str

class ReadmeResponse(BaseModel):
    readme: str
    suggested_badges: List[str]

@router.post("/generate", response_model=ReadmeResponse)
async def generate_readme(request: ReadmeRequest):
    try:
        # Combine file contents into a single string for the prompt
        files_content = "\n\n".join([f"--- {f.name} ---\n{f.content}" for f in request.files])
        
        user_prompt = get_readme_prompt(files_content, request.sections, request.template)
        readme_content = await claude_service.generate(README_SYSTEM_PROMPT, user_prompt)
        
        # Mock badges for now, or extract them from the generated content if possible
        suggested_badges = ["License: MIT", "Version: 1.0.0"]
        
        return ReadmeResponse(readme=readme_content, suggested_badges=suggested_badges)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
