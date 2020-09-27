import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/pre-tick', methods=['POST'])
def evaluate_pre_tick():
    file = request.files['data_file']
    logging.info("data sent for evaluation {}".format(file))

    result = 0

    logging.info("My result :{}".format(result))
    return json.dumps(result);



