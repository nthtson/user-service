variable "aws_region" {}
variable "cluster_name" {}
variable "db_name" {}
variable "db_user" {}
variable "db_password" {}
variable "vpc_id" {
  type        = string
  description = "VPC ID for EKS networking"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for EKS nodes"
}

variable "security_group_id" {}

variable "node_group_role_name" {
  type    = string
  default = "user-service-node-group-role"
}
variable "ec2_key_pair" {
  type        = string
  description = "EC2 key pair name for SSH access"
}