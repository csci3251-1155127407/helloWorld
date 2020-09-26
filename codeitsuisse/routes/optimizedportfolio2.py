import logging
import json,math
from flask import request, jsonify;
from codeitsuisse import app;
import numpy as np

logger = logging.getLogger(__name__)

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def my_round(n, places=0):
    if (places != 0):
        return normal_round((10 ** places) * n) / (10**places)
    else:
        return int(normal_round((10 ** places) * n) / (10**places) + 1e-6)

def calc(index_future):
    global portfolio
    global index_futures
    x = np.double(1) * portfolio["SpotPrcVol"] * index_future["CoRelationCoefficient"] / index_future["FuturePrcVol"]
    x = my_round(x, 3)
    x = max(x, 0)
    x = min(x, 1)
    y = np.double(1) * x * portfolio["Value"] / (index_future["IndexFuturePrice"] * index_future["Notional"])
    y = my_round(y)
    return x, y

@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimizedportfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    data = data["inputs"]
    result = {"outputs": []}
    for test in data:
        global portfolio
        global index_futures
        portfolio = test["Portfolio"]
        index_futures = test["IndexFutures"]

        best = ""
        best_x = np.double(0)
        best_y = np.double(0)
        for i in range(len(index_futures)):
            x, y = calc(index_futures[i])
            # print(F"x: {x}, y: {y}")
            EPS = 1e-12
            if (i == 0 or x < best_x or x == best_x and y < best_y):
            # if (i == 0 or x < best_x or math.fabs(x - best_x) <= EPS and y < best_y):
            # if (i == 0 or y < best_y or y == best_y and x < best_x):
            # if (i == 0 or x + index_futures[i]["FuturePrcVol"] < best_xp or x + index_futures[i]["FuturePrcVol"] == best_xp and y < best_y):
                best = index_futures[i]["Name"]
                best_x = x
                best_y = y
        result["outputs"] += [{"HedgePositionName": best, "OptimalHedgeRatio": best_x, "NumFuturesContract": best_y}]
    logging.info("My result :{}".format(result))
    return json.dumps(result)
