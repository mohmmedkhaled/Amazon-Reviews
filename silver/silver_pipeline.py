import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim
from pyspark.sql.functions import col, trim, substring, concat, lit

def create_spark_session():
    spark = SparkSession.builder \
        .appName("AmazonReviews-Silver-Pipeline") \
        .getOrCreate()
    return spark

def process_bronze_to_silver(spark, input_bronze_path, output_silver_path):
    try:
        print(f"🔄 Reading raw Parquet data from Bronze: {input_bronze_path} ...")
        
        # 1. read the raw Parquet data from the Bronze layer
        df_bronze = spark.read.parquet(input_bronze_path)
        
        initial_count = df_bronze.count()
        print(f"📊 Total records in Bronze layer: {initial_count}")
        
        # 2.(Transformation & Cleaning)
        print("🧼 Cleaning data, casting types, and truncating long text columns...")
        
        df_silver = df_bronze \
            .withColumn("rating", col("rating").cast("float")) \
            .withColumn("number_of_ratings", col("number_of_ratings").cast("integer")) \
            .withColumn("title", trim(col("title"))) \
            .filter(col("asin").isNotNull()) \
            .filter(col("title") != "") \
            .withColumn("title", concat(substring(col("title"), 1, 15), lit("..."))) \
            .withColumn("breadcrumbs", concat(substring(col("breadcrumbs"), 1, 10), lit("...")))
            
        # 3. Deduplication based on 'asin' (product ID)
        print("✨ Deduplicating records based on 'asin'...")
        df_silver = df_silver.dropDuplicates(["asin"])
            
        final_count = df_silver.count()
        print(f"📊 Total records after cleaning (Silver): {final_count}")
        print(f"🗑️ Removed {initial_count - final_count} duplicate or invalid rows.")
        
        print("📌 Final Silver Schema:")
        df_silver.printSchema()
        
        # 4. Writing the cleaned data to the Silver layer in Parquet format
        print(f"💾 Writing clean data to Silver layer: {output_silver_path} ...")
        df_silver.write \
            .mode("overwrite") \
            .parquet(output_silver_path)
            
        print("✅ Data successfully processed and written to Silver layer!")

    except Exception as e:
        print(f"❌ An error occurred during Silver processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    BUCKET_NAME = "amazon-reviews-lakehouse-bucket" 
    
    GCS_BRONZE_INPUT = f"gs://{BUCKET_NAME}/bronze/products_raw"
    GCS_SILVER_OUTPUT = f"gs://{BUCKET_NAME}/silver/products_clean"
    
    spark_session = create_spark_session()
    process_bronze_to_silver(spark_session, GCS_BRONZE_INPUT, GCS_SILVER_OUTPUT)