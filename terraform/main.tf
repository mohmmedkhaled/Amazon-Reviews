# (Data Lake Storage)
resource "google_storage_bucket" "lakehouse_bucket" {
  name          = var.bucket_name
  location      = var.gcp_region
  force_destroy = true 

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}

# Create Folders for Medallion Architecture inside the Bucket
resource "google_storage_bucket_object" "bronze_folder" {
  name    = "bronze/"
  content = " " # GCS does not have real folders, this creates a placeholder object to represent the folder
  bucket  = google_storage_bucket.lakehouse_bucket.name
}

resource "google_storage_bucket_object" "silver_folder" {
  name    = "silver/"
  content = " "
  bucket  = google_storage_bucket.lakehouse_bucket.name
}

resource "google_storage_bucket_object" "gold_folder" {
  name    = "gold/"
  content = " "
  bucket  = google_storage_bucket.lakehouse_bucket.name
}

# create a Dataproc cluster for Spark processing
resource "google_dataproc_cluster" "spark_cluster" {
  name   = "amazon-reviews-spark-cluster"
  region = var.gcp_region

  cluster_config {
    master_config {
      num_instances = 1
      machine_type  = "e2-standard-2" 
      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = 50
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = "e2-medium"
      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = 50
      }
    }

    software_config {
      image_version = "2.1-debian11"
    }
  }
}

# BigQuery Dataset (Gold Layer)
resource "google_bigquery_dataset" "gold_analytics_dataset" {
  dataset_id                  = "amazon_reviews_gold"
  friendly_name               = "Amazon Reviews Gold Analytics"
  description                 = "This dataset contains clean, aggregated tables for business intelligence and reporting."
  location                    = var.gcp_region
  delete_contents_on_destroy = true 
}