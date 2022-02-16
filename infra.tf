terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-2"
}

resource "aws_prometheus_workspace" "app-logging-data" {
  alias = "stock-predictions-prometheus"
}

resource "aws_dynamodb_table" "app-stock-predictions-api-StockPrices-table" {
  name           = "StockPrices"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "ticker"
  range_key      = "date"

  attribute {
    name = "ticker"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_dynamodb_table" "app-stock-predictions-api-SupportedCompanies-table" {
  name           = "SupportedCompanies"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "B3Code"

  attribute {
    name = "B3Code"
    type = "S"
  }
}

resource "aws_dynamodb_table" "app-stock-predictions-api-TrainingLog-table" {
  name           = "TrainingLog"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "model_file_name"

  attribute {
    name = "model_file_name"
    type = "S"
  }
}

resource "aws_dynamodb_table" "app-stock-predictions-api-PredictionHistories-table" {
  name           = "PredictionHistories"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "date"

  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_dynamodb_table" "app-stock-predictions-api-ApiCredentials-table" {
  name           = "ApiCredentials"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "ApiKey"

  attribute {
    name = "ApiKey"
    type = "S"
  }
}

resource "aws_s3_bucket" "b" {
  bucket = "stock-predictions"
  acl    = "private"
}
resource "aws_s3_bucket_object" "models-folder" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
  key    = "datasets/"
  source = "/dev/null"
}