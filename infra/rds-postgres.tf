resource "aws_db_instance" "postgres" {
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "14"
  instance_class         = "db.t3.micro"

  identifier             = "user-service-db"
  db_name                = var.db_name
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