# Makefile for Docker shorthand commands

# Image name
ECR=338791806049.dkr.ecr.eu-west-1.amazonaws.com/filip-capstone
TAG=0.0.4
IMAGE=$(ECR):$(TAG)
CONTAINER_NAME=capstone-project

build:
	docker build -t $(IMAGE) .

run: build
	docker run -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) -e AWS_REGION=$(AWS_REGION) --name $(CONTAINER_NAME) -it $(IMAGE)

login:
	aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $(ECR)

push: build login
	docker push $(IMAGE)