from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import lower, regexp_replace
from pyspark.ml.feature import Bucketizer, Tokenizer, StringIndexer
from pyspark.ml.feature import HashingTF, IDF, StopWordsRemover
from pyspark.ml import Pipeline

import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
stop_words = stopwords.words('english')

def read_spark_data(data_path):
  # Read data from data_path as  Spark DataFrame with columns defined below:
  #   - review_id: unique id of each review
  #   - user_id: user's id of reviewer
  #   - business_id: business the review is towards
  #   - stars: number of stars given by reviewer
  #   - text: review in text format
  spark = SparkSession.builder.appName("YelpReviewsSentimentAnalysis").getOrCreate()
  dataframe = spark.read.json(data_path)
  return dataframe.select("review_id", "stars", "text")


def preprocess(dataframe):
  # Preprocess with pipelines so the df will be ready for machine learning
  def clean_text(text):
    cl_txt = regexp_replace(text, "[^a-zA-Z\\s]", "")
    low_txt = lower(cl_txt)
    # remove stopwords
    no_stop_txt = regexp_replace(low_txt, r'\b(' + r'|'.join(stop_words) + r')\b\s*', "")
    return no_stop_txt

  df_clean = dataframe.select(
    'review_id',
    dataframe.stars.cast('float').alias('stars'),
    clean_text('text').alias('text')
  )

  # split into train and validation
  train_df, val_df = df_clean.randomSplit([0.8, 0.2], seed = 13517)

  ### PIPELINE
  # binning the review stars to be labels
  bucketizer = Bucketizer(splits=[0.0, 3.0, 5.0], inputCol="stars", outputCol="label")
  # process the text to be ready for ML
  tokenizer = Tokenizer(inputCol="text", outputCol="words")
  hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol='tf')
  idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5)
  pipeline = Pipeline(stages=[bucketizer, tokenizer, hashtf, idf])

  pipeline_fit = pipeline.fit(train_df) # only fit with train_data
  train_df = pipeline_fit.transform(train_df)
  val_df = pipeline_fit.transform(val_df) # use pipeline to transform val_df
  
  return train_df, val_df


if __name__ == "__main__":
  # use this main to test pyspark compatibility and data output.
  tmp_df = read_spark_data("../data/yelp_academic_dataset_review.json")
  train_df, val_df = preprocess(tmp_df)
  print(train_df.show(2))

  # expected output:
  # +--------------------+-----+--------------------+-----+--------------------+--------------------+--------------------+
  # |           review_id|stars|                text|label|               words|                  tf|            features|
  # +--------------------+-----+--------------------+-----+--------------------+--------------------+--------------------+
  # |--0TYNE-FwAHf34_X...|  5.0|location bit far ...|  1.0|[location, bit, f...|(65536,[1198,2408...|(65536,[1198,2408...|
  # |--4YXphzfj_JV7Mug...|  4.0|hot mess coming s...|  1.0|[hot, mess, comin...|(65536,[1257,1689...|(65536,[1257,1689...|
  # +--------------------+-----+--------------------+-----+--------------------+--------------------+--------------------+
  # only showing top 2 rows
