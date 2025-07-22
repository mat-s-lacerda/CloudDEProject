data "terraform_remote_state" "core" {
  backend = "gcs"

  config = {
    bucket = "de-analytics-meteo-dev-tfstate"
    prefix = "terraform/dev"
  }
}