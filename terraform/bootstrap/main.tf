# ---------------------------------------------------------------------------
# Bootstrap: cria o bucket S3 e a tabela DynamoDB que guardam o estado do
# Terraform de TODAS as cobras feitas com este template.
#
# Roda automaticamente no CD, antes do deploy da aplicação. Você não precisa
# executar nada aqui na mão.
# ---------------------------------------------------------------------------

terraform {
  backend "s3" {
    # Bucket "raiz", criado uma única vez na conta da Dev. É o mesmo usado
    # pelos outros templates — só a key muda, para não misturar os estados.
    bucket         = "battle-snake-bootstrap-state-new-account"
    dynamodb_table = "battle-snake-bootstrap-state-table-new-account"
    region         = "us-east-1"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

variable "project_name" {
  description = "Nome do repositório que está fazendo o deploy."
  type        = string
  default     = "battlesnake"
}

# Nomes de bucket S3 são únicos no mundo inteiro: por isso o sufixo do template.
resource "aws_s3_bucket" "terraform_state" {
  bucket = "battlesnake-python-template-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Trava o estado enquanto um deploy roda, para dois pushes ao mesmo tempo não
# corromperem o arquivo de estado.
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "battlesnake-python-template-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}

output "s3_bucket_name" {
  description = "Bucket S3 que guarda o estado do Terraform das aplicações."
  value       = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  description = "Tabela DynamoDB usada para travar o estado durante o deploy."
  value       = aws_dynamodb_table.terraform_locks.name
}
