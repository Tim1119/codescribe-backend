CHANGELOG_SYSTEM_PROMPT = """You are an expert release manager. Your task is to analyze code changes and generate a professional changelog."""

def get_changelog_prompt(old_code: str, new_code: str, format: str) -> str:
    return f"""Compare the following two versions of code and generate a changelog in {format} format.

OLD CODE:
```
{old_code}
```

NEW CODE:
```
{new_code}
```

Return a JSON object with the following structure:
{{
    "changelog": "The full changelog text (markdown)",
    "version_suggestion": "Suggested semantic version (e.g. 1.2.0)",
    "breaking_changes": ["Breaking change 1", "Breaking change 2"]
}}
"""
