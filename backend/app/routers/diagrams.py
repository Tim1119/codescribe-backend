from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
from app.services.claude_service import ClaudeService
from app.prompts.diagrams_prompts import DIAGRAMS_SYSTEM_PROMPT, get_diagram_prompt

router = APIRouter()
claude_service = ClaudeService()

class FileContent(BaseModel):
    name: str
    content: str

class DiagramRequest(BaseModel):
    files: List[FileContent]
    diagram_type: str

class DiagramResponse(BaseModel):
    mermaid_code: str
    description: str

@router.post("/generate", response_model=DiagramResponse)
async def generate_diagram(request: DiagramRequest):
    try:
        files_content = "\n\n".join([f"--- {f.name} ---\n{f.content}" for f in request.files])
        user_prompt = get_diagram_prompt(files_content, request.diagram_type)
        response_text = await claude_service.generate(DIAGRAMS_SYSTEM_PROMPT, user_prompt)
        
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return DiagramResponse(**data)
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            # Fallback if parsing fails, assuming the whole text might be the code or description
            return DiagramResponse(
                mermaid_code="graph TD;\n    A[Error] --> B[Could not parse response];",
                description="Failed to generate diagram."
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
