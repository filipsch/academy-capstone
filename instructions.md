## All instruction

Create a .env file (not in git) with the AWS creds.

Run docker:

```
TAG=0.0.3
IMAGE=338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone
FULL_TAG=$IMAGE:$TAG
docker build -t $FULL_TAG .
docker run -it $FULL_TAG
```

Create private ECR repository:

```
# Create repo (run once)
aws ecr create-repository --repository-name filip-capstone-2

# Authenticate docker
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $IMAGE

# Push the docker image
docker push $FULL_TAG
```

Create Batch Job Definition

```
aws batch register-job-definition --job-definition-name Filip-capstone-job-definition --tags '{"environment": "academy-capstone-winter-2024"}' --type container --container-properties '{ "image": "338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone-2:0.0.1", "executionRoleArn": "arn:aws:iam::338791806049:role/academy-capstone-winter-2024/academy-capstone-winter-2024-batch-job-role", "jobRoleArn": "arn:aws:iam::338791806049:role/academy-capstone-winter-2024/academy-capstone-winter-2024-batch-job-role", "resourceRequirements": [ { "type": "VCPU", "value": "1" }, { "type": "MEMORY", "value": "2048" }]}'

aws batch submit-job --job-name Filip-capstone-job --job-queue academy-capstone-winter-2024-job-queue --job-definition Filip-capstone-job-definition --tags '{"environment": "academy-capstone-winter-2024"}'
```

Schedule through AWS

```
aws s3 cp my_dag.py dataminded-academy-capstone-resources/dags/dag_filip.py
```
