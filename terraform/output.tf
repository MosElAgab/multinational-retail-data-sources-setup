output "rds_endpoint" {
  value = aws_db_instance.rds_instance.endpoint
}
output "rds_vpc_id" {
  value = aws_security_group.rds_sg.vpc_id
}
