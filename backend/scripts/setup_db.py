import boto3
import os


def create_tables():
    """Template for creating DynamoDB tables"""
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        # Development credentials only - use AWS IAM roles in production
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )

    # Example table structure - modify for your needs
    table = dynamodb.create_table(
        TableName="example_table",
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

    print(f"Created table: {table.table_name}")


if __name__ == "__main__":
    create_tables()
