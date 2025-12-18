README_SYSTEM_PROMPT = """You are an expert at creating clear, comprehensive README files for software projects. You analyze code to understand project structure, purpose, and usage."""

def get_readme_prompt(files_content: str, sections: list, template: str) -> str:
    sections_str = ", ".join(sections)
    return f"""Analyze the following project files and generate a {template} README.md.

Include these sections: {sections_str}

PROJECT FILES:
{files_content}

Generate a professional README.md that would help developers understand and use this project.
Return ONLY the markdown content of the README.md file."""
