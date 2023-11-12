from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id

def load(dataset="dbfs:/FileStore/Jaxon-Yue-Individual-Project-3/wages_1.csv", 
         dataset2="dbfs:/FileStore/Jaxon-Yue-Individual-Project-3/wages_2.csv"):
    spark = SparkSession.builder.appName("Read CSV").getOrCreate()
    # load csv and transform it by inferring schema
    wages_1_df = spark.read.csv(dataset, header=True, inferSchema=True)
    wages_2_df = spark.read.csv(dataset2, header=True, inferSchema=True)

    # add unique IDs to the DataFrames
    wages_1_df = wages_1_df.withColumn("id", monotonically_increasing_id())
    wages_2_df = wages_2_df.withColumn("id", monotonically_increasing_id())

    # transform into a delta lakes table and store it 
    wages_1_df.write.format("delta").mode("overwrite").saveAsTable("wages_1_delta")
    wages_2_df.write.format("delta").mode("overwrite").saveAsTable("wages_2_delta")
    
    num_rows = wages_1_df.count()
    print(num_rows)
    num_rows = wages_2_df.count()
    print(num_rows)
    
    return "Completed transform and load"

if __name__ == "__main__":
    load()