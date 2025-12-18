from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import documentation, readme, api_docs, explainer, diagrams, qa, changelog, health

app = FastAPI(title="DocuMint API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documentation.router, prefix="/api/documentation", tags=["Documentation"])
app.include_router(readme.router, prefix="/api/readme", tags=["README"])
app.include_router(api_docs.router, prefix="/api/api-docs", tags=["API Docs"])
app.include_router(explainer.router, prefix="/api/explainer", tags=["Explainer"])
app.include_router(diagrams.router, prefix="/api/diagrams", tags=["Diagrams"])
app.include_router(qa.router, prefix="/api/qa", tags=["Q&A"])
app.include_router(changelog.router, prefix="/api/changelog", tags=["Changelog"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
