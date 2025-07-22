resource "google_secret_manager_secret" "bucket_name" {
  secret_id = "${var.env}-infra-data-safekeeping-bucket"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "bucket_name" {
  secret      = google_secret_manager_secret.bucket_name.id
  secret_data = module.buckets["infra_data_safekeeping"].bucket_name
}
