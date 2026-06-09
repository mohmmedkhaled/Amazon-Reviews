import sys
from pyspark.sql import SparkSession

def create_spark_session():

    spark = SparkSession.builder \
        .appName("AmazonReviews-Bronze-Pipeline") \
        .getOrCreate()
    return spark

def process_csv_to_bronze(spark, input_csv_path, output_bronze_path):
    try: 
        print(f"🔄 Reading raw data from: {input_csv_path} ...")
        
        # read the raw CSV data
        df_raw = spark.read \
            .option("header", "true") \
            .option("escape", '"') \
            .csv(input_csv_path)
        
        print("📊 Data Schema:")
        df_raw.printSchema()
        
        print(f"💾 Writing data in Parquet format to Bronze layer: {output_bronze_path} ...")
        
        # write the data in Parquet format to the Bronze layer
        df_raw.write \
            .mode("overwrite") \
            .parquet(output_bronze_path)
        
        print("✅ Data successfully written to Bronze layer!")

    except Exception as e:
        print(f"❌ An error occurred during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":

    BUCKET_NAME = "amazon-reviews-lakehouse-bucket" 
    
    # GCS paths for input CSV and Bronze output
    GCS_INPUT_CSV = f"gs://{BUCKET_NAME}/data/products.csv" 
    GCS_BRONZE_PATH = f"gs://{BUCKET_NAME}/bronze/products_raw"
    
    spark_session = create_spark_session()
    process_csv_to_bronze(spark_session, GCS_INPUT_CSV, GCS_BRONZE_PATH)