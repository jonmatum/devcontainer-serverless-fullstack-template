# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Template")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check endpoint - useful for AWS Lambda/API Gateway"""
    return {"message": "API Template Ready", "version": "1.0.0", "status": "healthy"}


@app.get("/example")
async def example_endpoint():
    """Example endpoint structure with AWS best practices"""
    return {"message": "Replace with your business logic"}
