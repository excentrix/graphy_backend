from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import upload_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with the specific origins allowed in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the upload router
app.include_router(upload_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Infographic AI API"}