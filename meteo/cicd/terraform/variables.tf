variable "project_id" {
  type        = string
  default     = "analytics-meteorology-dev"
  description = "The GCP project ID to deploy resources into."
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "The GCP region for deploying resources."

  validation {
    condition     = contains(["us-central1", "europe-west1", "southamerica-east1"], var.region)
    error_message = "Region must be one of us-central1, europe-west1, or southamerica-east1."
  }
}

variable "credentials_file" {
  type        = string
  default     = "~/.gcp_sa_keys/sa-terraform-dev.json"
  description = "Path to the service account JSON key file."
}
