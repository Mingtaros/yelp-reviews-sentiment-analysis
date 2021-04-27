import fire
import numpy as np
import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer


def main(model_name = 'logisticregresion', infile='data/processed/test_review.csv', outfile='data/processed/pred_sentiment.csv'):
    """
    Restaurant Sentiment Analysis

    Usage: python main.py --model_name=<model_name> --infile=<infile_path> --outfile=<outfile_path>

    Run model <model_name> to generate sentiment in <outfile> using provided texts in <infile>
    <outfile> and <infile> in csv format

    All argument optional
    """
    cv = pickle.load(open('model/countvectorizer.sav', 'rb'))
    model = pickle.load(open('model/' + model_name + '.sav', 'rb'))

    reviews = pd.read_csv(infile).iloc[:, 0].values
    reviews = cv.transform(reviews).toarray()

    sentiment = model.predict(reviews)

    sentiment_dataframe = pd.DataFrame(data={
        'sentiment' : sentiment
    })

    sentiment_dataframe.to_csv(outfile, index=False, header=True)

    print("success")

if __name__ == '__main__':
    fire.Fire(main)