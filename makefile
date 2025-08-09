# Project configuration
PROJECT_NAME = multinational-retail-data-sources-setup
ENV ?= dev
TF_ENV = $(ENV).tfvars

# Defined targets
.PHONY: test terraform-init terraform-plan terraform-apply terraform-destroy terraform-output terraform-format
#
test:
	PYTHONPATH=$(shell pwd) pytest -v

# 
terraform-init:
	terraform -chdir=terraform init

# 
terraform-plan:
	terraform -chdir=terraform plan -var-file="$(TF_ENV)"

# 
terraform-apply:
	terraform -chdir=terraform apply -var-file="$(TF_ENV)"

# 
terraform-destroy:
	terraform -chdir=terraform destroy -var-file="$(TF_ENV)"

# 
terraform-output:
	terraform -chdir=terraform output

# 
terraform-format:
	terraform -chdir=terraform fmt


# terraform apply -chdir=terraform -var-file="dev.tfvars"
# terraform output -json > data_sources_outputs.json

# install dependencies in local file
# pip install -r requirements.txt -t .

# zip everthinng indide lamda function folder
# zip -r9 get_number_of_stores.zip . -x "*__pycache__*"

# zip sepecific file
# zip -r9 get_number_of_stores.zip lambda_function.py

# test api
# curl -i -H "X-API-KEY: [x-api-key]" [number_of_stores_url]