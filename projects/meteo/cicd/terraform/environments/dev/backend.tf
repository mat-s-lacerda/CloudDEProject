terraform {
  backend "gcs" {
    bucket  = "de-analytics-meteo-dev-tfstate"
    prefix  = "terraform/dev"
  }
}
