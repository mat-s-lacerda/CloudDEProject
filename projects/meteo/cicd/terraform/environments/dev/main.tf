locals {
  default_buckets = {
    batch_data_intake = {
      name          = "${var.project_id}-batch-data-intake"
      location      = "${var.region}"
      force_destroy = true
      labels = {
        env  = "${var.env}"
        type = "raw"
      }
    }
  }

  resolved_buckets = length(var.buckets) > 0 ? var.buckets : local.default_buckets
}

module "buckets" {
  for_each = local.resolved_buckets

  source        = "../../modules/google_cloud_storage"
  name          = each.value.name
  location      = each.value.location
  project_id    = var.project_id
  force_destroy = each.value.force_destroy
  labels        = each.value.labels
}
