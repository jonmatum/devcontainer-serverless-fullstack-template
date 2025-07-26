import boto3
import os
import time
from botocore.exceptions import ClientError


def create_counter_table():
    """Create the counter table for the template demonstration"""
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        # Development credentials only - use AWS IAM roles in production
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )

    table_name = os.getenv("TABLE_NAME", "counter_table")

    try:
        # Check if table already exists
        existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
        if table_name in existing_tables:
            print(f"Table '{table_name}' already exists. Skipping creation.")
            return

        # Create the counter table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        print(f"Creating table '{table_name}'...")
        
        # Wait for table to be created
        table.wait_until_exists()
        print(f"Table '{table_name}' created successfully!")

        # Initialize the global counter
        table.put_item(
            Item={
                "id": "global_counter",
                "count": 0,
                "updated_at": "initialized"
            }
        )
        print("Counter initialized to 0")

    except ClientError as e:
        print(f"Error creating table: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


def create_example_table():
    """Template for creating additional DynamoDB tables - users can modify this"""
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )

    table_name = "example_table"

    try:
        existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
        if table_name in existing_tables:
            print(f"Table '{table_name}' already exists. Skipping creation.")
            return

        # Example table structure - modify for your needs
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "sort_key", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "sort_key", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        print(f"Creating example table '{table_name}'...")
        table.wait_until_exists()
        print(f"Example table '{table_name}' created successfully!")

    except ClientError as e:
        print(f"Error creating example table: {e}")
    except Exception as e:
        print(f"Unexpected error creating example table: {e}")


def main():
    """Main function to set up all required tables"""
    print("Setting up DynamoDB tables for DevContainer Template...")
    
    try:
        # Create the main counter table for the demo
        create_counter_table()
        
        # Create example table (optional - users can uncomment if needed)
        # create_example_table()
        
        print("\nDatabase setup completed successfully!")
        print("You can now use the counter API endpoints:")
        print("   GET  /api/counter - Get current count")
        print("   POST /api/counter - Increment count")
        print("   DELETE /api/counter - Reset count")
        
    except Exception as e:
        print(f"\nDatabase setup failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
