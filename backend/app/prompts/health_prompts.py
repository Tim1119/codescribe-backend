HEALTH_SYSTEM_PROMPT = """You are an expert code quality analyst. Your task is to evaluate the quality of code documentation and provide a health score."""

def get_health_prompt(code: str) -> str:
    return f"""Analyze the documentation quality of the following code.

CODE:
```
{code}
```

Evaluate based on:
1. Completeness (Are all functions/classes documented?)
2. Clarity (Is the documentation easy to understand?)
3. Accuracy (Does it match the code?)
4. Coverage (Percentage of code documented)

Return a JSON object with the following structure:
{{
    "score": 85,
    "breakdown": {{
        "completeness": 90,
        "clarity": 80,
        "accuracy": 85,
        "coverage": 85
    }},
    "suggestions": [
        {{ "title": "Missing docstring", "description": "Add docstring to function 'process_data'", "line": 15 }},
        {{ "title": "Unclear parameter", "description": "Clarify 'type' parameter in 'User' class", "line": 42 }}
    ]
}}
"""
