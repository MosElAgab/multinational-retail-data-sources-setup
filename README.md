# multinational-retail-data-sources-setup
multinational-retail-data-sources



<!-- TODO -->
<!-- define terraform version -->
<!-- explicitly set RDS to default vpc; can be done by linking security group to default vpc; check docs -->
<!-- define password validation for variables.tf/db_password to enhance security -->
<!-- for prodcution, consider using TF_VAR_db_password or AWS secret manager -->

# summary of work done
- Makefile for terraform commands
- terraform script to create rds with credential place in dev.tfvars; SG to allow access using creds defined; rds endpoint outputs on terminal
- upload_user_data.py developed to connect to rds db created and uploads user data; it uses creds in .env
- uploads_card_details_data.py developed to create s3 bucket, uploads card_details.pdf data; and generates pre-signed url for get request access; pre-signed url ouputs on terminal
- upload_store_data developed to upload legacy_store.csv

# Next
## move s3 bucket createtion to terraform
Easier teardown and management.

## develop api to inetract with store_data 
this will involve: 
- API gateway, s3 lambda and aws cloud watch for logging; 
- creating a policy to get store data from s3 bucket and attach it to a role that can be assumend by lambda;
- create a policy to allows sending lambda logs to cloud watch; creating lambda function for get number of how many stores and get store by id;
- creating rest api in api gatways;
- creating a resource with /number_of_stores resource path and get method to invoke get_number_of_stores lambda function;
- creating a resource with /store_details resource path with path parameter /store_details/{store_id} and get method to invoke get_store_by_id lambda function;

- developing lambda function locally and uploading, maybe later done within terraform