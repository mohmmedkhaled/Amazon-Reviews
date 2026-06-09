import sys
from pyspark.sql import SparkSession

def create_spark_session():
   
    spark = SparkSession.builder \
        .appName("AmazonReviews-Gold-Pipeline") \
        .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.30.0") \
        .getOrCreate()
    return spark

def process_silver_to_gold(spark, input_silver_path, bq_dataset, bq_table_name, bucket_name):
    try:
        print(f"🔄 Reading clean Parquet data from Silver: {input_silver_path} ...")
        
        # 1. read the cleaned data from the Silver layer
        df_silver = spark.read.parquet(input_silver_path)
        
        print("💡 Performing analytics aggregations for Gold Layer...")
        # filtering top-rated products with at least 1000 ratings
        df_gold_top_products = df_silver.filter("rating >= 4.0 AND number_of_ratings > 1000")
        
        print(f"📊 Total curated records for Gold Table: {df_gold_top_products.count()}")
        
        # 2. BigQuerys requires a temporary GCS bucket for staging data during the load process
        temporary_gcs_bucket = f"{bucket_name}"
        
        # 3. Writing data directly to BigQuery Table
        print(f"💾 Loading data into BigQuery table: {bq_dataset}.{bq_table_name} ...")
        
        df_gold_top_products.write \
            .format("bigquery") \
            .option("table", f"{bq_dataset}.{bq_table_name}") \
            .option("temporaryGcsBucket", temporary_gcs_bucket) \
            .mode("overwrite") \
            .save()
            
        print("🏆 Data successfully loaded into BigQuery Gold Layer!")

    except Exception as e:
        print(f"❌ An error occurred during Gold processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # the variables
    PROJECT_ID = "my-project-771277"
    BUCKET_NAME = "amazon-reviews-lakehouse-bucket"
    
    GCS_SILVER_INPUT = f"gs://{BUCKET_NAME}/silver/products_clean"
    BQ_DATASET = "amazon_reviews_gold"
    BQ_TABLE_NAME = "top_rated_products"
    
    spark_session = create_spark_session()
    process_silver_to_gold(spark_session, GCS_SILVER_INPUT, f"{PROJECT_ID}.{BQ_DATASET}", BQ_TABLE_NAME, BUCKET_NAME)