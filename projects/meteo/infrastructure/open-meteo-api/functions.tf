data "google_secret_manager_secret_version" "bucket_name" {
  secret  = "${var.env}-infra-data-safekeeping-bucket"
  project = "${var.project_id}"
  version = "latest"
}

locals {
  bucket_name = data.google_secret_manager_secret_version.bucket_name.secret_data

  default_functions = {
    api_to_gcs = {
      name        = "analytics-weather-data-forecast-api-extractor-dev"
      source_dir  = "../../initiatives/open-meteo-api/crf/api_to_gcs"
      entry_point = "entrypoint"
      location    = "${var.region}"
      description = "API to GCS"
      project_id  = "${var.project_id}"
      zip_path    = "/tmp/api_to_gcs.zip"
      env_vars = {
        ENV        = "${var.env}"
        PROJECT_ID = "${var.project_id}"
      }
      source_bucket = "${local.bucket_name}"
      source_object = "api_to_gcs.zip"
    }
    #gcs_to_bq = {
    #  name         = "analytics-weather-data-forecast-gcs-to-bq-dev"
    #  entry_point  = "entrypoint"
    #  zip_path     = "${path.module}/../../../../src/crf/gcs_to_bq/function.zip"
    #  env_vars     = {
    #    PROJECT_ID = "${var.project_id}"
    #  }
    #}
  }

  resolved_functions = length(var.functions) > 0 ? var.functions : local.default_functions
}

data "archive_file" "functions" {
  for_each    = local.resolved_functions
  type        = "zip"
  output_path = each.value.zip_path
  source_dir  = each.value.source_dir
}

resource "google_storage_bucket_object" "function_code_zip" {
  for_each = local.resolved_functions

  name   = each.value.source_object
  bucket = each.value.source_bucket
  source = each.value.zip_path
}

module "functions" {
  for_each = local.resolved_functions

  source = "../modules/cloud_run_function"

  name          = each.value.name
  location      = each.value.location
  description   = each.value.description
  project_id    = var.project_id
  entry_point   = each.value.entry_point
  source_bucket = each.value.source_bucket
  source_object = each.value.source_object
  env_vars      = each.value.env_vars
}
