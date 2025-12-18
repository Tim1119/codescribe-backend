EXPLAINER_SYSTEM_PROMPT = """You are an expert code instructor and technical communicator. Your task is to explain code concepts clearly and accurately, adapting to the requested audience level."""

def get_explainer_prompt(code: str, level: str, focus_area: str = None) -> str:
    focus_str = f"Focus particularly on: {focus_area}" if focus_area else ""
    
    return f"""Explain the following code for a "{level}" audience.
{focus_str}

CODE:
```
{code}
```

Return a JSON object with the following structure:
{{
    "explanation": "Main explanation text (markdown supported)",
    "key_concepts": ["Concept 1", "Concept 2"],
    "analogies": ["Analogy 1", "Analogy 2"]
}}
"""
