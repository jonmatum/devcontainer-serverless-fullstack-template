# backend/app/main.py
import os
import boto3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from botocore.exceptions import ClientError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DevContainer Template API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DynamoDB configuration - template users can easily modify these
DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://dynamodb-local:8000")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
TABLE_NAME = os.getenv("TABLE_NAME", "counter_table")

# Initialize DynamoDB client
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT,
    region_name=AWS_REGION,
    # Development credentials - use IAM roles in production
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "dummy"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "dummy"),
)

# Pydantic models for request/response validation
class CounterResponse(BaseModel):
    count: int
    message: str
    timestamp: str

class CounterUpdate(BaseModel):
    increment: int = 1


@app.get("/")
def root():
    """Health check endpoint - useful for AWS Lambda/API Gateway"""
    return {
        "message": "DevContainer Template API Ready", 
        "version": "1.0.0", 
        "status": "healthy",
        "endpoints": {
            "counter": "/api/counter",
            "health": "/",
            "docs": "/docs"
        }
    }


@app.get("/api/counter", response_model=CounterResponse)
async def get_counter():
    """Get current counter value from DynamoDB"""
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.get_item(Key={"id": "global_counter"})
        
        if "Item" in response:
            count = response["Item"]["count"]
            timestamp = response["Item"]["updated_at"]
        else:
            # Initialize counter if it doesn't exist
            count = 0
            timestamp = "never"
            
        return CounterResponse(
            count=count,
            message="Counter retrieved successfully",
            timestamp=timestamp
        )
        
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/counter", response_model=CounterResponse)
async def increment_counter(update: CounterUpdate = CounterUpdate()):
    """Increment counter value in DynamoDB"""
    try:
        from datetime import datetime
        
        table = dynamodb.Table(TABLE_NAME)
        timestamp = datetime.utcnow().isoformat()
        
        # Use atomic counter increment for thread safety
        response = table.update_item(
            Key={"id": "global_counter"},
            UpdateExpression="ADD #count :increment SET updated_at = :timestamp",
            ExpressionAttributeNames={"#count": "count"},
            ExpressionAttributeValues={
                ":increment": update.increment,
                ":timestamp": timestamp
            },
            ReturnValues="ALL_NEW"
        )
        
        new_count = response["Attributes"]["count"]
        
        logger.info(f"Counter incremented to {new_count}")
        
        return CounterResponse(
            count=new_count,
            message=f"Counter incremented by {update.increment}",
            timestamp=timestamp
        )
        
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/api/counter")
async def reset_counter():
    """Reset counter to zero - useful for template demonstration"""
    try:
        from datetime import datetime
        
        table = dynamodb.Table(TABLE_NAME)
        timestamp = datetime.utcnow().isoformat()
        
        table.put_item(
            Item={
                "id": "global_counter",
                "count": 0,
                "updated_at": timestamp
            }
        )
        
        logger.info("Counter reset to 0")
        
        return CounterResponse(
            count=0,
            message="Counter reset successfully",
            timestamp=timestamp
        )
        
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
