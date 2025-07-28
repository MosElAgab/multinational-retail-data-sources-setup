# Project configuration
PROJECT_NAME = multinational-retail-data-sources-setup
ENV ?= dev
TF_ENV = $(ENV).tfvars

# Defined targets
.PHONY: terraform-init terraform-plan terraform-apply terraform-destroy terraform-output terraform-format
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