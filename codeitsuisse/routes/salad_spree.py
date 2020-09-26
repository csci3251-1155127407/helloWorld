import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluate_salad_spree():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_salads");
    street_map = data.get("salad_prices_street_map")
    res = 1e9

    for street in street_map:
        for i in range(len(street) - n + 1):
            sum = 0
            flag = 0
            for j in range(n):
                if street[i + j] == 'X':
                    flag = 1
                    break
                sum += int(street[i + j])

            if not flag:
                res = min(res, sum)

    if res == 1e9:
        res = 0

    result = {"result" : res}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



