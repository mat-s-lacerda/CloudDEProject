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

variable "core_infra_bucket" {
  description = "Name of the GCS bucket"
  type        = string
}

variable "core_infra_prefix" {
  description = "Prefix of the GCS bucket"
  type        = string
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

variable "functions" {
  description = "(Optional) Custom Function config. If empty, a default one is generated."
  type = map(object({
    name          = string
    entry_point   = string
    zip_path      = string
    env_vars      = map(string)
    source_dir    = string
    location      = string
    description   = string
    project_id    = string
    source_bucket = string
    source_object = string
  }))
  default = {}
}