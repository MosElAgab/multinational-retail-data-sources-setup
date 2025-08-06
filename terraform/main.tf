# Security group for PostgreSQL access
resource "aws_security_group" "rds_sg" {
  name        = "rds-access"
  description = "Allow PostgreSQL access"


  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# RDS PostgreSQL instance
resource "aws_db_instance" "rds_instance" {
  engine                   = "postgres"
  engine_version           = "17.4"
  identifier               = var.rds_identifier
  username                 = var.db_username
  password                 = var.db_password
  instance_class           = "db.t3.micro"
  allocated_storage        = 5
  storage_type             = "gp2"
  network_type             = "IPV4"
  publicly_accessible      = true
  vpc_security_group_ids   = [aws_security_group.rds_sg.id]
  delete_automated_backups = true
  skip_final_snapshot      = true

  db_name = var.db_name
  port    = 5432

  tags = {
  Project = "multinational-retail"
  Owner   = "Mostafa"
}

}


# S3 Bucket

resource "aws_s3_bucket" "multinational_retail_bucket" {
    bucket = var.s3_bucket_name
    force_destroy = true
    tags = {
        Project = "multinational_retail_data_sources_setup"
    }
}


#lambda

## Iam role
# refactor to use json file
resource "aws_iam_role" "lambda_exec_role" {
  name = "Store_data_inetraction_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
      Statement = [{
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }]
  })
}

## Attach plocies to role
# allow cloud watch logs
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# allow s3 read only access
resource "aws_iam_role_policy_attachment" "lambda_s3_read_access" {
  role = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}


## lambda resource
resource "aws_lambda_function" "get_number_of_stores" {
  function_name = "get_number_of_stores"
  role = aws_iam_role.lambda_exec_role.arn
  handler = "lambda_function.lambda_handler"
  runtime = "python3.12"
  timeout = 30

  filename = "${path.module}/../lambda/get_number_of_stores/get_number_of_stores.zip"
  source_code_hash = filebase64sha256(
    "${path.module}/../lambda/get_number_of_stores/get_number_of_stores.zip"
  )

  environment {
    variables = {
      BUCKET_NAME = var.s3_bucket_name
      STORE_CSV_OBJECT_KEY = var.store_csv_object_key
    }
  }

  tags = {
  Project = "multinational-retail"
  Owner   = "Mostafa"
}

}
