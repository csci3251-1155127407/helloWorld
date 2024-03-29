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

    cost = {
        "maPomegranate" : 95,
        "maRamubutan" : 97,
        "maWatermelon" : 20,
        "maApple" : 71,
        "maAvocado" : 73,
        "maPineapple" : 48
    }

    result = 0

    for item in data:
        result += cost[item] * data[item]

    logging.info("My result :{}".format(result))
    return json.dumps(result);



