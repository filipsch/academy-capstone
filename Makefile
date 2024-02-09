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

install_conveyor:
	sudo wget https://app.conveyordata.com/api/info/cli/location/linux/amd64 -O conveyor_linux_amd64.tar.gz
	sudo tar -zxvf conveyor_linux_amd64.tar.gz
	sudo chmod +x bin/linux/amd64/conveyor
	sudo cp bin/linux/amd64/conveyor /usr/local/bin/conveyor

convey:
	conveyor project create --name filip-capstone-project
	conveyor project build
	conveyor project run --env winterschool2024
	conveyor project deploy --env winterschool2024