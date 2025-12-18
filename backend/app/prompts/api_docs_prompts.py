API_DOCS_SYSTEM_PROMPT = """You are an expert API documentation writer. Your task is to analyze code and generate OpenAPI-compatible documentation."""

def get_api_docs_prompt(code: str, framework: str) -> str:
    return f"""Analyze the following {framework} code and extract all API endpoints.
Generate a JSON object containing a list of endpoints with their methods, paths, parameters, and descriptions.
Also generate a markdown summary of the API.

CODE:
```{framework}
{code}
```

Return a JSON object with the following structure:
{{
    "endpoints": [
        {{
            "method": "GET|POST|PUT|DELETE",
            "path": "/path/to/endpoint",
            "summary": "Brief summary",
            "parameters": [
                {{ "name": "param_name", "in": "query|path|body", "type": "string|int", "required": true }}
            ],
            "responses": {{ "200": "Description" }}
        }}
    ],
    "documentation": "Markdown documentation here..."
}}
"""
