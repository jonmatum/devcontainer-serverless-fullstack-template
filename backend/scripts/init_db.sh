#!/bin/bash

# Database initialization script for DevContainer Template
# This script sets up the DynamoDB tables after containers are running

echo "Initializing DynamoDB tables..."

# Wait for DynamoDB Local to be ready
echo "Waiting for DynamoDB Local to be ready..."
sleep 5

# Set environment variables for the script
export DYNAMODB_ENDPOINT="http://localhost:${DYNAMODB_PORT:-8000}"
export AWS_REGION="us-east-1"
export TABLE_NAME="counter_table"

# Run the Python setup script
cd /app && python scripts/setup_db.py

echo "Database initialization completed!"
