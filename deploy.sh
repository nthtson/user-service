#!/bin/bash
set -e

echo "Initializing Terraform..."
cd infra
terraform init
terraform apply -auto-approve
cd ..

echo "Deploying Helm Chart..."
helm upgrade --install user-service ./helm-chart --namespace default

echo "Done! Check your resources with kubectl get all"
