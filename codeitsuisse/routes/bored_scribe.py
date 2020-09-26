import logging
import json

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = []

    print(len(data))
    for test in data:
        print(test["encryptedText"])

    logging.info("My result :{}".format(result))
    return json.dumps(result);



