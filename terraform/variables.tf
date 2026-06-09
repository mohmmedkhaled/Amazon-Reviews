variable "gcp_project_id" {
  description = "The ID of the GCP Project"
  type        = string
}

variable "gcp_region" {
  description = "The region to deploy resources in"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "The name of the GCS bucket for Medallion layers"
  type        = string
}