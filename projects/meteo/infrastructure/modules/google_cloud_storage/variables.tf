variable "name" {
  description = "Name of the GCS bucket"
  type        = string
}

variable "location" {
  description = "GCP region where the bucket will be created"
  type        = string
}

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "force_destroy" {
  description = "Allow deleting a non-empty bucket"
  type        = bool
  default     = false
}

variable "labels" {
  description = "Labels to apply to the bucket"
  type        = map(string)
  default     = {}
}
