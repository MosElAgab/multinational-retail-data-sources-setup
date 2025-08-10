output "rds_endpoint" {
  value = aws_db_instance.rds_instance.endpoint
}
output "rds_vpc_id" {
  value = aws_security_group.rds_sg.vpc_id
}
output "number_of_stores_url" {
  value = "https://${aws_api_gateway_rest_api.store_api.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.store_api_stage.stage_name}/number_of_stores"
}
