# Amazon-Reviews
An end-to-end E-commerce Data Lakehouse built on GCP using Terraform, Apache Spark (Dataproc), and BigQuery, culminating in an interactive Power BI dashboard.

# Amazon Product Reviews - End-to-End Data Lakehouse Pipeline

An enterprise-grade, automated Data Lakehouse platform built using a modern data engineering stack on Google Cloud Platform (GCP). The pipeline ingests raw Amazon product review datasets, processes them using a three-tier Medallion Architecture (Bronze, Silver, Gold), and delivers business-ready insights via an interactive Power BI Dashboard.

## 🏗️ Architecture Overview

The project implements Infrastructure as Code (IaC) to provision cloud resources and automates data orchestration seamlessly:

1. **Infrastructure as Code:** Provisioned GCP buckets, Dataproc clusters, and BigQuery datasets using **Terraform**.
2. **Orchestration:** Directed DAG execution and workflows via **Cloud Composer (Apache Airflow)**.
3. **Ingestion (Bronze Layer):** Loads raw Amazon CSV data into Google Cloud Storage (GCS) in an immutable Parquet format.
4. **Transformation & Cleaning (Silver Layer):** PySpark processing on a **Cloud Dataproc** cluster to handle data types, perform deduplication based on unique IDs (`asin`), and clean heavily cluttered text descriptions via truncation to optimize downstream analytical performance.
5. **Aggregations & Modeling (Gold Layer):** Computes key metrics and populates finalized business schemas within **Google BigQuery**.
6. **BI Analytics:** Serves business-driven Key Performance Indicators (KPIs) through a dynamic **Power BI Dashboard**.

---

## 🛠️ Tech Stack & Tools

* **Cloud Provider:** Google Cloud Platform (GCP)
* **Infrastructure as Code:** Terraform
* **Workflow Orchestration:** Apache Airflow / Cloud Composer
* **Distributed Computing Engine:** Apache Spark (PySpark) / Cloud Dataproc
* **Data Warehouse / Lakehouse:** Google BigQuery
* **Storage:** Google Cloud Storage (GCS)
* **Business Intelligence:** Power BI Desktop

---

## 📊 Data Model & Feature Engineering (DAX)

To transition raw metrics into actionable business value, advanced data modeling techniques were introduced in Power BI:
* **Product_Class:** A calculated DAX feature to segment high-performing products (`Top Tier`) from stable ones based on customer ratings.
* **Popularity_Score:** A specialized business metric integrating total rating volume against average scores to properly weigh authentic market demand.

---

## 🚀 Key Learning Outcomes

* Configured scalable distributed Spark environments by dynamically upgrading infrastructure to manage high-volume string transformations without Out-of-Memory (OOM) failures.
* Implemented production-ready PySpark text preprocessing including substring truncations and conditional data query sanitization.
* Established secure credential management by isolating production environment pipelines from version control tracking.

##  E-Commerce Customer Sentiment & Product Analytics

<img width="808" height="404" alt="Dashboard" src="https://github.com/user-attachments/assets/d25894d6-7209-4a12-b798-dff016600fb3" />

