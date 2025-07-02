variable "name" {
  description = "Name of the GCS bucket"
  type        = string
}

variable "location" {
  description = "GCP region where the bucket will be created"
  type        = string
}

variable "description" {
  description = "Description of the GCS bucket"
  type        = string
  default     = "Cloud Function deployed via Terraform"
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "entry_point" {
  description = "Name of the function entry point"
  type        = string
}

variable "source_bucket" {
  description = "Name of the GCS bucket"
  type        = string
}

variable "source_object" {
  description = "Name of the Object inside the bucket"
  type        = string
}

variable "env_vars" {
  description = "Environment variables for the function"
  type        = map(string)
  default     = {}
}

variable "labels" {
  description = "Labels to apply to the bucket"
  type        = map(string)
  default     = {}
}
