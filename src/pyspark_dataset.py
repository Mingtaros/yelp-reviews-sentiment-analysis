from pyspark.sql import SparkSession


def read_spark_data(data_path):
  # Read data from data_path as Spark DataFrame with columns defined below:
  #   - review_id: unique id of each review
  #   - user_id: user's id of reviewer
  #   - business_id: business the review is towards
  #   - stars: number of stars given by reviewer
  #   - text: review in text format
  spark = SparkSession.builder.appName("YelpReviewsSentimentAnalysis").getOrCreate()
  dataframe = spark.read.json(data_path)
  return dataframe.select("review_id", "user_id", "business_id", "stars", "text")


if __name__ == "__main__":
  tmp_df = read_spark_data("../data/yelp_academic_dataset_review.json")
  print(tmp_df.show(2))
