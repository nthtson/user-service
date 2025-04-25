resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks.arn
  vpc_config {
    subnet_ids = var.subnet_ids

    # Optional but helpful if you're using public subnets for simplicity
    endpoint_public_access = true
    endpoint_private_access = false
  }

  tags = {
    Name = "user-service-cluster"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster,
    aws_iam_role_policy_attachment.eks_service
  ]
}