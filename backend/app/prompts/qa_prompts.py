QA_SYSTEM_PROMPT = """You are an expert coding assistant. Your task is to answer questions about the provided code context accurately and helpfully."""

def get_qa_prompt(question: str, code_context: str, history: list) -> str:
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    
    return f"""Answer the following question based on the provided code context.

CODE CONTEXT:
{code_context}

CHAT HISTORY:
{history_str}

QUESTION:
{question}

Return a JSON object with the following structure:
{{
    "answer": "The answer to the question (markdown supported)",
    "code_references": [
        {{ "file": "filename", "line_start": 10, "line_end": 20, "snippet": "code snippet" }}
    ]
}}
"""
