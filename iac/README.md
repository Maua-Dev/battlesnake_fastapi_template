# Battlesnake CDK (Python)

Infrastructure for deploying the Battlesnake FastAPI app as an AWS Lambda Function URL.

## Requirements

- Python 3.13
- Node.js (for the CDK CLI)
- AWS credentials with permission to deploy to the target account

## Setup

```bash
python3.13 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
npm install -g aws-cdk@2.1140.0
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `AWS_ACCOUNT_ID_DEV` | Target AWS account (dev) |
| `AWS_REGION` | Deploy region (`sa-east-1`) |
| `STACK_NAME` | CloudFormation stack name |
| `PROJECT_NAME` | Resource naming prefix |
| `GITHUB_REF_NAME` | Git branch / stage name |

## Useful commands

```bash
cdk synth    # synthesize CloudFormation
cdk deploy   # deploy the stack
cdk diff     # compare with deployed stack
cdk destroy  # tear down the stack
```

The stack creates a Lambda (Python 3.13), a public Function URL, and a CloudWatch alarm that notifies the existing `sns-battlesnake` SNS topic.
