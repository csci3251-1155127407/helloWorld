import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data();
    logging.info("data sent for evaluation {}".format(data))
    data = json.loads(data.decode("utf-8"))

    # apple = data['maApple']
    # watermelon = data['maWatermelon']
    # banana = data['maBanana']
    #
    # a = 75
    # w = 64
    # b = 32
    #
    # result = a * apple + w * watermelon + b * banana
    result = 0
    logging.info("My result :{}".format(result))
    return json.dumps(result);



