resource "aws_security_group" "rds" {
  name        = "rds-sg"
  description = "Allow RDS access from EKS nodes"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # TODO: Replace with actual EKS node SG or IP later
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-sg"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "14"
  instance_class         = "db.t3.micro"

  identifier             = "user-service-db"       # ✅ required
  db_name                = var.db_name             # ✅ actual DB name
  username               = var.db_user
  password               = var.db_password

  publicly_accessible     = true
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name

  skip_final_snapshot    = true
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = var.subnet_ids
  tags = {
    Name = "rds-subnet-group"
  }
}