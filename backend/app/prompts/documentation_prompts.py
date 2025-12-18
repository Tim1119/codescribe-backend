DOCUMENTATION_SYSTEM_PROMPT = """You are an expert technical documentation writer. Your task is to add comprehensive documentation to source code.

Guidelines:
- Add docstrings to all functions, classes, and methods
- Include parameter descriptions with types
- Document return values
- Add inline comments for complex logic
- Follow the specified documentation style exactly
- Preserve all original code functionality
- Be concise but thorough"""

def get_documentation_prompt(code: str, language: str, style: str) -> str:
    return f"""Document the following {language} code using {style} style documentation.

CODE:
```{language}
{code}
```

Return the fully documented code with all docstrings and comments added. Do not include any markdown formatting or explanations outside the code block. Just return the code."""
