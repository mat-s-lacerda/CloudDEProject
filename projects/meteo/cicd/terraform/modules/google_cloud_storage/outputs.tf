output "bucket_name" {
  description = "The name of the GCS bucket"
  value       = google_storage_bucket.default.name
}

output "bucket_self_link" {
  description = "Self-link of the GCS bucket"
  value       = google_storage_bucket.default.self_link
}
