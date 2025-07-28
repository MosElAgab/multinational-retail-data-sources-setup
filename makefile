# Project configuration
PROJECT_NAME = multinational-retail-data-sources-setup

# Defined targets
.PHONY: tarraform-init terraform-plan terraform-apply terraform-destroy, terraform-output

# 
terraform-init:
	terraform -chdir=terraform init

# 
terraform-plan:
	terraform -chdir=terraform plan

# 
terraform-apply:
	terraform -chdir=terraform apply

# 
terraform-destroy:
	terraform -chdir=terraform destroy

# 
terraform-output:
	terraform -chdir=terraform output