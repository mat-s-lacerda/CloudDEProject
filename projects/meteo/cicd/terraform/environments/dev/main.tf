provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "bkt_batch_data_intake" {
  name     = "${var.project_id}-batch-data-intake"
  location = var.region
}
