resource "google_storage_bucket" "default" {
  name          = var.name
  location      = var.location
  project       = var.project_id
  force_destroy = var.force_destroy
  labels        = var.labels

  uniform_bucket_level_access = true
}
