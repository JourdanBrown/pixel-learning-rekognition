# Pixel Learning Co. - Rekognition Image Classification Pipeline

Automated image classification system using Amazon Rekognition, S3, DynamoDB, and GitHub Actions.

## Architecture Overview

- **GitHub Actions**: Automates CI/CD pipeline
- **Amazon S3**: Stores images for analysis
- **Amazon Rekognition**: Detects and classifies objects in images
- **DynamoDB**: Stores analysis results (separate tables for beta/prod)

## AWS Resources

- **S3 Bucket**: `pixel-learning-rekognition-bucket`
- **DynamoDB Tables**: `beta_results` and `prod_results`
- **IAM Policy**: `pixel-learning`

## How It Works

### Pull Request (Beta Environment)
1. Create a new branch
2. Add images to `images/` folder
3. Create Pull Request to `main`
4. GitHub Actions automatically:
   - Uploads images to S3
   - Analyzes with Rekognition
   - Saves results to `beta_results` table

### Merge to Main (Production Environment)
1. Merge Pull Request
2. GitHub Actions automatically:
   - Re-analyzes images
   - Saves results to `prod_results` table

## Usage

### Adding New Images

1. Create a new branch:
   - Click "main" dropdown → "View all branches"
   - Click "New branch"
   - Name: `add-images-YOURNAME`

2. Upload images:
   - Navigate to `images/` folder
   - Click "Add file" → "Upload files"
   - Drag and drop your .jpg or .png files
   - Commit changes

3. Create Pull Request:
   - Click "Pull requests" tab
   - Click "New pull request"
   - Select your branch
   - Click "Create pull request"
   - Wait for GitHub Actions to complete

4. Review results in AWS DynamoDB `beta_results` table

5. Merge Pull Request when ready

## Project Structure
```
pixel-learning-rekognition/
├── .github/
│   └── workflows/
│       ├── on_pull_request.yml
│       └── on_merge.yml
├── images/
│   └── (your image files)
├── scripts/
│   └── analyze_image.py
├── requirements.txt
└── README.md
```

## Viewing Results

### AWS Console
1. Go to DynamoDB
2. Select `beta_results` or `prod_results` table
3. Click "Explore table items"

### Example Result
```json
{
  "filename": "rekognition-input/balloon.jpg",
  "labels": [
    {"Name": "Balloon", "Confidence": 98.49},
    {"Name": "Aircraft", "Confidence": 98.46}
  ],
  "timestamp": "2025-06-01T14:55:32Z",
  "branch": "add-images-john"
}
```

## GitHub Secrets Required

The following secrets must be configured in Settings → Secrets and variables → Actions:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `S3_BUCKET`
- `DYNAMODB_TABLE_BETA`
- `DYNAMODB_TABLE_PROD`

## Troubleshooting

- Check GitHub Actions logs for errors
- Verify AWS credentials in secrets
- Ensure DynamoDB tables exist
- Check S3 bucket permissions

---

**Pixel Learning Co.** | Powered by AWS Rekognition
```

5. Scroll down and click **"Commit changes"**
6. Click **"Commit changes"** in popup

---

## **Phase 8: Test the Setup**

### **Step 1: Create a Test Branch**

1. Click on **"main"** dropdown (near top-left)
2. Type a new branch name: `test-workflow`
3. Click **"Create branch: test-workflow from main"**

### **Step 2: Add a Test Image**

1. Make sure you're on the `test-workflow` branch (check the dropdown)
2. Navigate to the `images/` folder
3. Click **"Add file"** → **"Upload files"**
4. **Drag and drop** a test image (.jpg or .png)
   - Any image will work - try a photo of a balloon, car, cat, etc.
5. Click **"Commit changes"**
6. Click **"Commit changes"** in the popup

### **Step 3: Create Pull Request**

1. You should see a yellow banner saying "test-workflow had recent pushes"
2. Click **"Compare & pull request"**
3. **Title:** `Test image analysis workflow`
4. Click **"Create pull request"**

### **Step 4: Watch GitHub Actions Run**

1. You should see a yellow dot next to your PR
2. Click on **"Details"** next to the check
3. Watch the workflow execute:
   - Checkout code ✓
   - Set up Python ✓
   - Install dependencies ✓
   - Configure AWS credentials ✓
   - Analyze images ✓

### **Step 5: Check Results in DynamoDB**

1. Go to AWS Console → DynamoDB
2. Click on `beta_results` table
3. Click **"Explore table items"**
4. You should see your image analysis result!

### **Step 6: Merge and Test Production**

1. Go back to your Pull Request
2. Click **"Merge pull request"**
3. Click **"Confirm merge"**
4. Check the **"Actions"** tab - production workflow should run
5. Check `prod_results` table in DynamoDB

---

## **Your Repository Structure Should Look Like:**
```
pixel-learning-rekognition/
├── .github/
│   └── workflows/
│       ├── on_pull_request.yml ✅
│       ├── on_merge.yml ✅
│       └── placeholder.txt (can delete)
├── images/
│   ├── .gitkeep
│   └── your-test-image.jpg ✅
├── scripts/
│   ├── .gitkeep
│   └── analyze_image.py ✅
├── .gitignore ✅
├── README.md ✅
└── requirements.txt ✅
