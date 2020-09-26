import logging
import json
import collections

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/swaphedge', methods=['POST'])
def evaluate_swaphedge():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    order = data.get("order")
    print(data)
    result = {"order": order}

    logging.info("My result :{}".format(result))
    return json.dumps(result);



