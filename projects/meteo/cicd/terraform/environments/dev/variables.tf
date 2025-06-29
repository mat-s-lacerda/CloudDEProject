variable "env" {
  type        = string
  description = "The environment to deploy resources into."
}

variable "project_id" {
  type        = string
  description = "The GCP project ID to deploy resources into."
}

variable "region" {
  type        = string
  description = "The GCP region for deploying resources."

  validation {
    condition     = contains(["us-central1", "europe-west1", "southamerica-east1"], var.region)
    error_message = "Region must be one of us-central1, europe-west1, or southamerica-east1."
  }
}

variable "buckets" {
  description = "(Optional) Custom bucket config. If empty, a default one is generated."
  type = map(object({
    name          = string
    location      = string
    force_destroy = bool
    labels        = map(string)
  }))
  default = {}
}