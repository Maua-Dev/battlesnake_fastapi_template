# ---------------------------------------------------------------------------
# Aplicação: publica a sua cobra como uma função Lambda exposta por um
# API Gateway. Roda automaticamente no CD — você não precisa mexer aqui.
#
# No fim do deploy, o output "api_url_base" mostra a URL para cadastrar no
# site do Battlesnake.
# ---------------------------------------------------------------------------

terraform {
  backend "s3" {
    # bucket, dynamodb_table e key são preenchidos pelo CD
    # (veja .github/workflows/CD.yaml, passo "Terraform Init").
    region  = "us-east-1"
    encrypt = true
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

locals {
  function_name = "${var.project_name}-lambda-${var.environment}"

  # Zip com src/ + as bibliotecas do requirements.txt, montado pelo CD
  # (veja .github/workflows/CD.yaml, job "build_python").
  artifact_path = "../../build/battlesnake.zip"
}

# ------------------------------- Lambda ------------------------------------

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_role_battlesnake-${var.project_name}_${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Permite que a função escreva logs no CloudWatch.
resource "aws_iam_role_policy_attachment" "lambda_exec_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Criado antes da função para podermos limitar a retenção dos logs. Sem isso a
# AWS cria o grupo sozinha e guarda os logs para sempre.
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = 14
}

resource "aws_lambda_function" "battlesnake" {
  function_name = local.function_name

  filename         = local.artifact_path
  source_code_hash = filebase64sha256(local.artifact_path)

  role = aws_iam_role.lambda_role.arn

  # "src.main.handler" = o objeto `handler` (o Mangum) exportado por src/main.py.
  runtime       = "python3.12"
  handler       = "src.main.handler"
  architectures = ["arm64"]

  timeout     = 10
  memory_size = 512

  depends_on = [aws_cloudwatch_log_group.lambda]
}

# ----------------------------- API Gateway ---------------------------------

resource "aws_api_gateway_rest_api" "api" {
  name        = "api-battlesnake-${var.project_name}-${var.environment}"
  description = "API da cobra ${var.project_name} (Python)"
}

# {proxy+} captura /start, /move, /end e qualquer outra rota que você criar.
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

# A raiz "/" precisa de um método próprio: é a rota de informações da cobra.
resource "aws_api_gateway_method" "root" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_rest_api.api.root_resource_id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.proxy.http_method

  # AWS_PROXY sempre invoca a Lambda via POST, independente do método original.
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.battlesnake.invoke_arn
}

resource "aws_api_gateway_integration" "root" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_rest_api.api.root_resource_id
  http_method = aws_api_gateway_method.root.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.battlesnake.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayToInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.battlesnake.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

# Publica a configuração acima. O "triggers" força um redeploy sempre que
# alguma das rotas muda.
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.proxy.id,
      aws_api_gateway_method.proxy.id,
      aws_api_gateway_integration.proxy.id,
      aws_api_gateway_method.root.id,
      aws_api_gateway_integration.root.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.proxy,
    aws_api_gateway_integration.root,
  ]
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = var.environment
}

# ------------------------------- Outputs -----------------------------------

output "api_url_base" {
  description = "URL da sua cobra. É esta que você cadastra no site do Battlesnake."
  value       = aws_api_gateway_stage.stage.invoke_url
}

output "cloudwatch_logs" {
  description = "Link direto para os logs da sua cobra."
  value       = "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/${replace(aws_cloudwatch_log_group.lambda.name, "/", "$252F")}"
}
