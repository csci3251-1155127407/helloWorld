import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data();
    logging.info("data sent for evaluation {}".format(data))
    apple = data.get('maApple')
    watermelon = data.get('maWatermelon')
    banana = data.get('maBanana')

    a = 75
    w = 64
    b = 32

    result = a * apple + w * watermelon + b * banana
    logging.info("My result :{}".format(result))
    return json.dumps(result);



