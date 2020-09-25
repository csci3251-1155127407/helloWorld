import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/sorting', methods=['POST'])
def evaluate_sorting():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputArray = data.get("input");
    result = sorted(inputArray)
    logging.info("My result :{}".format(result))
    return json.dumps(result);



