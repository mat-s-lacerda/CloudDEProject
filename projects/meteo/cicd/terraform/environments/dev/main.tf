provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "example" {
  name     = "${var.project_id}-example-bucket"
  location = var.region
}


resource "google_storage_bucket" "example1" {
  name     = "${var.project_id}-example-bucket1"
  location = var.region
}