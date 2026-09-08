variable "project_name" {
  type        = string
  description = "Nome único desta instância do projeto. Usado para nomear os recursos na AWS."
}

variable "environment" {
  type        = string
  description = "Ambiente do deploy (ex.: 'dev', 'staging', 'prod')."
  default     = "dev"
}
