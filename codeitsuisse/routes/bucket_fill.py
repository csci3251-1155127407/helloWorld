import logging
import json
import collections

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/bucket-fill', methods=['POST'])
def evaluate_bucket():
    data = request.get_data()
    logging.info("data sent for evaluation {}".format(data))

    result = 0

    logging.info("My result :{}".format(result))
    return json.dumps(result);



