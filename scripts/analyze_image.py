import boto3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

def upload_to_s3(file_path, bucket_name, s3_key):
    """Upload image to S3 bucket"""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"✓ Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
        return True
    except Exception as e:
        print(f"✗ Error uploading to S3: {e}")
        return False

def analyze_image_with_rekognition(bucket_name, s3_key):
    """Analyze image using Amazon Rekognition"""
    rekognition_client = boto3.client('rekognition')
    
    try:
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': s3_key
                }
            },
            MaxLabels=10,
            MinConfidence=75
        )
        
        labels = [
            {
                'Name': label['Name'],
                'Confidence': round(label['Confidence'], 2)
            }
            for label in response['Labels']
        ]
        
        print(f"✓ Detected {len(labels)} labels")
        return labels
    except Exception as e:
        print(f"✗ Error analyzing image: {e}")
        return []

def save_to_dynamodb(table_name, filename, labels, branch):
    """Save analysis results to DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    item = {
        'filename': filename,
        'labels': labels,
        'timestamp': timestamp,
        'branch': branch
    }
    
    try:
        table.put_item(Item=item)
        print(f"✓ Saved results to DynamoDB table: {table_name}")
        print(f"  Record: {json.dumps(item, indent=2)}")
        return True
    except Exception as e:
        print(f"✗ Error saving to DynamoDB: {e}")
        return False

def process_images(images_dir, bucket_name, dynamodb_table, branch_name):
    """Process all images in the specified directory"""
    image_extensions = {'.jpg', '.jpeg', '.png'}
    images_path = Path(images_dir)
    
    if not images_path.exists():
        print(f"✗ Images directory not found: {images_dir}")
        return False
    
    image_files = [
        f for f in images_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    if not image_files:
        print(f"⚠ No images found in {images_dir}")
        return True
    
    print(f"\n{'='*60}")
    print(f"Processing {len(image_files)} image(s) from {images_dir}")
    print(f"Branch: {branch_name}")
    print(f"Target Table: {dynamodb_table}")
    print(f"{'='*60}\n")
    
    success_count = 0
    
    for image_file in image_files:
        print(f"\n--- Processing: {image_file.name} ---")
        
        s3_key = f"rekognition-input/{image_file.name}"
        
        if not upload_to_s3(str(image_file), bucket_name, s3_key):
            continue
        
        labels = analyze_image_with_rekognition(bucket_name, s3_key)
        if not labels:
            print("⚠ No labels detected or error occurred")
            continue
        
        if save_to_dynamodb(dynamodb_table, s3_key, labels, branch_name):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully processed {success_count}/{len(image_files)} images")
    print(f"{'='*60}\n")
    
    return success_count == len(image_files)

if __name__ == "__main__":
    bucket_name = os.environ.get('S3_BUCKET')
    dynamodb_table = os.environ.get('DYNAMODB_TABLE')
    branch_name = os.environ.get('GITHUB_REF_NAME', 'unknown')
    images_dir = os.environ.get('IMAGES_DIR', 'images')
    
    if not bucket_name or not dynamodb_table:
        print("✗ Error: S3_BUCKET and DYNAMODB_TABLE environment variables must be set")
        sys.exit(1)
    
    success = process_images(images_dir, bucket_name, dynamodb_table, branch_name)
    
    sys.exit(0 if success else 1)
