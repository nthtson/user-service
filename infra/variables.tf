variable "aws_region" {}
variable "cluster_name" {}
variable "vpc_id" {}
variable "subnet_ids" { type = list(string) }
variable "db_name" {}
variable "db_user" {}
variable "db_password" {}
variable "security_group_id" {}