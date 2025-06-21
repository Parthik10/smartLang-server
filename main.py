from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from routes import translate, report

app = FastAPI(
    title="SmartLang API",
    description="A compiler-based English to Spanish translation API",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://smart-lang.netlify.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(translate.router)
app.include_router(report.router)

@app.get("/")
async def root():
    return {"message": "Welcome to SmartLang API. Use /docs for documentation."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's assigned port
    uvicorn.run("main:app", host="0.0.0.0", port=port)