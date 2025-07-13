resource "google_cloudfunctions2_function" "default" {
  name        = var.name
  location    = var.location
  description = var.description
  project     = var.project_id
  labels      = var.labels
  build_config {
    runtime     = "python312"
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = var.source_bucket
        object = var.source_object
      }
    }
  }
  service_config {
    available_memory      = "256M"
    timeout_seconds       = 60
    environment_variables = var.env_vars
  }
}
