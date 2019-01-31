import numpy as np
import boto3
import pickle
from flask import Flask, request, json
from flask_cors import CORS
from memoized import memoized

BUCKET_NAME = 'non-hacker-news-models'
MODEL_FILE_NAME = 'NB_model.pkl'
T_VECTORIZER_FILE_NAME = 't_vectorizer.pkl'
U_VECTORIZER_FILE_NAME = 'u_vectorizer.pkl'

app = Flask(__name__)
CORS(app)

S3 = boto3.client('s3', region_name='us-east-1')


@app.route('/', methods=['POST'])
def index():
    """
    Serve prediction requests, incoming request body looks like:

    '{"data":[["python hacker c++", "github"], ["trump wall politics", "nytimes"]]}'

    :return: serialized predictions (probabilities in range [0,1] for each class)
    :rtype: str(dict)) of the form {'prediction': [[0.108, 0.892], [0.356, 0.644]]}
    """
    body_dict = request.get_json(silent=True)
    data = body_dict['data']

    model = load(MODEL_FILE_NAME)
    t_vectorizer = load(T_VECTORIZER_FILE_NAME)
    u_vectorizer = load(U_VECTORIZER_FILE_NAME)

    titles = [title_url_pair[0] for title_url_pair in data]
    urls = [title_url_pair[1] for title_url_pair in data]

    title_matrix = t_vectorizer.transform(titles).toarray()
    url_matrix = u_vectorizer.transform(urls).toarray()

    X = np.concatenate([title_matrix, url_matrix], axis=1)

    prediction = model.predict_proba(X).tolist()
    result = {'prediction': prediction}

    return json.dumps(result)

@memoized
def load(f_name):
    response = S3.get_object(Bucket=BUCKET_NAME, Key=f_name)

    v_str = response['Body'].read()
    loaded = pickle.loads(v_str)
    return loaded

if __name__ == '__main__':
    app.run(host='0.0.0.0')
