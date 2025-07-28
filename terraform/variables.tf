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

variable "db_identifier" {
  description = "Identifier name for the RDS instance"
  type        = string
  default     = "mydb"
}

variable "db_name" {
  description = "Database name for the RDS instance db created at launch"
  type        = string
  default     = "mydb"
}
