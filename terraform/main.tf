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
  engine             = "postgres"
  engine_version     = "17.4"
  identifier         = "multinational-retail"
  username           = "retail_admin"
  password           = "retail_admin_1234"
  instance_class     = "db.t3.micro"
  allocated_storage  = 5
  storage_type      = "gp2"
  network_type      = "IPV4"
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  delete_automated_backups = true
  skip_final_snapshot = true

  db_name               = "retail"
  port               = 5432
}
