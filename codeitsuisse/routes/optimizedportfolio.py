import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def calc(index_future):
    global portfolio
    global index_futures
    x = portfolio["SpotPrcVol"] * index_future["CoRelationCoefficient"] / index_future["FuturePrcVol"]
    x = round(x, 3)
    y = x * portfolio["Value"] / (index_future["IndexFuturePrice"] * index_future["Notional"])

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
        best_x = -1
        best_y = -1
        for i in range(len(index_futures)):
            x, y = calc(index_futures[i])
            if ((best_x == -1 or x < best_x) or (x == best_x and y < best_y)):
                best = index_futures[i]["Name"]
                best_x = x
                best_y = y


        result["outputs"] += [{"HedgePositionName": best, "OptimalHedgeRatio": round(best_x, 3), "NumFuturesContract": round(best_y)}]


    logging.info("My result :{}".format(result))
    return json.dumps(result)