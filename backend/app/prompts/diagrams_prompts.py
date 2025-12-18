DIAGRAMS_SYSTEM_PROMPT = """You are an expert software architect and Mermaid.js specialist. Your task is to analyze code and generate Mermaid diagrams that accurately represent the system structure."""

def get_diagram_prompt(files_content: str, diagram_type: str) -> str:
    return f"""Analyze the following project files and generate a {diagram_type} using Mermaid syntax.

PROJECT FILES:
{files_content}

Return a JSON object with the following structure:
{{
    "mermaid_code": "The mermaid diagram code (string)",
    "description": "A brief description of the diagram"
}}
"""
