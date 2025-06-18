provider "google" {
  credentials = file("/home/msl/terraform-user-dev-key.json")
  project     = "analytics-meteorology-dev"
  region      = "us-central1"
}

resource "google_storage_bucket" "my_bucket" {
  name     = "my-first-tf-bucket-123456"
  location = "us-central1"
}
