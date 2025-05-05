from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import debate

app = FastAPI(title="Gemini Debator API")
# 👇 Add this to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the debate router
app.include_router(prefix="/api",router=debate.router)
