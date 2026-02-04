# Linear regression

# create files  : generate-data.py
import time
import random
from datetime import datetime
while True:
    with open("data/stream/censor.csv", "a") as f:
        temp = round(random.uniform(20, 40), 2)
        f.write(f"{datetime.now()},{temp}\n")
    time.sleep(1)

#spark_demp.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
# Spark Session
spark = (
    SparkSession.builder
    .appName("Live Spark ML Example - Train Once")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
# Feature Assembler (shared)
assembler = VectorAssembler(
    inputCols=["temperature"],
    outputCol="features"
)
# TRAIN MODEL (RUNS ONLY ONCE)
def train_model():
    print("Training model ONLY ONCE")
    train_data = spark.createDataFrame(
        [(25.0, 25.1), (30.0, 30.1), (35.0, 35.0)],# demo data for training
        ["temperature", "label"]
    )
    train_features = assembler.transform(train_data)
    lr = LinearRegression(
        featuresCol="features",
        labelCol="label"
    )
    return lr.fit(train_features) #train with data [(25.0, 25.1), (30.0, 30.1), (35.0, 35.0)]
model = train_model()
# STREAMING DATA
schema = "timestamp STRING, temperature DOUBLE"
stream_df = (
    spark.readStream
    .schema(schema)
    .csv("data/stream")
)
feature_df = assembler.transform(stream_df)
# APPLY MODEL
predictions = model.transform(feature_df)# predict the temperature
query = (
    predictions
    .select(
        col("timestamp"),
        col("temperature"),
        round(col("prediction"), 2).alias("prediction")
    )
    .writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", "false")
    .option("numRows", 100)
    .start()
)
query.awaitTermination()


# Logistic regression

# create files  : generate-data.py
import time
import random
from datetime import datetime
while True:
    with open("data/stream2/censor.csv", "a") as f:
        temp = round(random.uniform(20, 40), 2)
        f.write(f"{datetime.now()},{temp}\n")
    time.sleep(1)

#spark_demp.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
# Spark Session
spark = (
    SparkSession.builder
    .appName("Live Spark ML Example - Train Once")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
# Feature Assembler (shared)
assembler = VectorAssembler(
    inputCols=["temperature"],
    outputCol="features"
)
# TRAIN MODEL (RUNS ONLY ONCE)
def train_model():
    print("Training model ONLY ONCE")
    train_data = spark.createDataFrame(
        [(0, 0), (1,0), (2, 0), (3, 0), (4, 0), (5, 1), (6, 1), (7, 1), (8, 1)],# demo data for training
        ["temperature", "label"]
    )
    train_features = assembler.transform(train_data)
    lr = LinearRegression(
        featuresCol="features",
        labelCol="label"
    )
    return lr.fit(train_features) #train with data [(25.0, 25.1), (30.0, 30.1), (35.0, 35.0)]
model = train_model()
# STREAMING DATA
schema = "temperature INT"
stream_df = (
    spark.readStream
    .schema(schema)
    .csv("data/stream2")
)
feature_df = assembler.transform(stream_df)
# APPLY MODEL
predictions = model.transform(feature_df)# predict the temperature
query = (
    predictions
    .select(
        col("temperature"),
        round(col("prediction"), 2).alias("prediction")
    )
    .writeStream
    .outputMode("append")
    .format("console")
    .option("truncate", "false")
    .option("numRows", 100)
    .start()
)
query.awaitTermination()
