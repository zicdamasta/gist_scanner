terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.13.0"
    }
  }
}

provider "google" {
  project = local.project_id
  region = local.region
  zone = local.zone
  credentials = "key.json"
}