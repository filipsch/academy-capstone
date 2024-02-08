## All instruction

Create a .env file (not in git) with the AWS creds.

Run docker:

```
docker build -t capstone .
docker run capstone .
```

Create private ECR repository:

```
# Create repo (run once)
aws ecr create-repository --repository-name filip-capstone --image-scanning-configuration scanOnPush=true --encryption-configuration encryptionType=KMS --image-tag-mutability IMMUTABLE

# Authenticate docker
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone

# Tag the docker image
docker tag capstone 338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone:0.0.1

# Push the docker image
docker push 338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone:0.0.1
```

Create Batch Job Definition

```
aws batch register-job-definition --job-definition-name filip-capstone-job-definition --type container --container-properties '{ "image": "338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone:0.0.1", "jobRoleArn": "arn:aws:iam::338791806049:role/academy-capstone-winter-2024/academy-capstone-winter-2024-batch-job-role"}'
```
