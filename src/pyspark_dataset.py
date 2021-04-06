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
  # use this main to test pyspark compatibility and data output.
  tmp_df = read_spark_data("../data/yelp_academic_dataset_review.json")
  print(tmp_df.show(2))

  # expected output:
  # +--------------------+--------------------+--------------------+-----+--------------------+
  # |           review_id|             user_id|         business_id|stars|                text|
  # +--------------------+--------------------+--------------------+-----+--------------------+
  # |lWC-xP3rd6obsecCY...|ak0TdVmGKo4pwqdJS...|buF9druCkbuXLX526...|  4.0|Apparently Prides...|
  # |8bFej1QE5LXp4O05q...|YoVfDbnISlW0f7abN...|RA4V8pr014UyUbDvI...|  4.0|This store is pre...|
  # +--------------------+--------------------+--------------------+-----+--------------------+
  # only showing top 2 rows
