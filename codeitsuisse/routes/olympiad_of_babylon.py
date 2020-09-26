import logging
import json

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_olympiad_of_babylon():
    data = request.get_data();
    logging.info("data sent for evaluation {}".format(data))
    result = []

    logging.info("My result :{}".format(result))
    return json.dumps(result);



