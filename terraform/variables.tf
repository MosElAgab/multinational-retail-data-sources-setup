variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-2"
}

variable "aws_profile" {
  description = "AWS CLI profile name"
  type        = string
  default     = "default"
}

variable "stage" {
  type = string
  description = "stage name e.g, dev or prod"
}

variable "db_username" {
  description = "Username for the RDS PostgreSQL instance"
  type        = string
  default     = "postgres"
}


variable "db_password" {
  description = "User password for RDS PostgreSQL instance"
  type        = string
  default     = "postgres"
  sensitive   = true
}

variable "rds_identifier" {
  description = "Identifier name for the RDS instance"
  type        = string
  default     = "mydb"
}

variable "db_name" {
  description = "Database name for the RDS instance db created at launch"
  type        = string
  default     = "mydb"
}

variable "s3_bucket_name" {
    type = string
    description = "name of s3 bucket for storing project data on aws"
}

variable "store_csv_object_key" {
  type = string
  description = "name of store csv file object stored in the s3"
}


variable "store_api_key_name" {
  type = string
  sensitive   = true
  description = "aws api gateway api key name"
}

variable "store_api_key_value" {
  type = string
  sensitive   = true
  description = "aws api gateway api key"
}