locals {
  project_id = "de-analytics-meteo-dev"
  region     = "us-central1"
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.3.0"
}

provider "google" {
  project = local.project_id
  region  = local.region
}
