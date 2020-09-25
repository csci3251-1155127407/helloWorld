import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/encryption', methods=['POST'])
def evaluate_encryption():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = []

    for input in data:
        n = input.get("n")
        text = input.get("text")

        processed_text = [ch for ch in text if ch.isalnum()]
        res = ["" for i in range(len(processed_text))]

        cur = 0
        start = 1

        for i in range(len(processed_text)):
            res[cur] += processed_text[i].upper()
            cur = cur + n
            if cur >= len(processed_text):
                cur = start
                start = start + 1

        result.append('+'.join(res))

    logging.info("My result :{}".format(result))
    return json.dumps(result);



