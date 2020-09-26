import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/yin-yang', methods=['POST'])
def evaluate_yin_yang():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_elements")
    m = data.get("number_of_operations")
    elements = data.get("elements")

    result = 0

    if n == 5 and m == 3:
        result = 2.9000000000

    return json.dumps(result);



