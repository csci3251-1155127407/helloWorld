import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def calc(index_future):
    global portfolio
    global index_futures
    x = portfolio["SpotPrcVol"] * index_future["CoRelationCoefficient"] / index_future["FuturePrcVol"]
    y = round(x, 3) * portfolio["Value"] / (index_future["IndexFuturePrice"] * index_future["Notional"])

    # x = max(x, 0)
    # x = min(x, 1)

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
        best_x = 9e18
        best_y = 9e18

        # lowest future vasidjhasd
        best1 = ""
        best_x1 = 9e18
        best_y1 = 9e18
        best_z1 = 9e18

        for i in range(len(index_futures)):
            x, y = calc(index_futures[i])
            z = index_futures[i]["FuturePrcVol"]

            print(F"x: {x}, y: {y}")
            if (x < best_x or (x == best_x and y < best_y)):
                best = index_futures[i]["Name"]
                best_x = x
                best_y = y

            if (z < best_z1 or (z == best_z1 and y < best_y1)):
                best1 = index_futures[i]["Name"]
                best_x1 = x
                best_y1 = y
                best_z1 = z


        if best_y1 < best_y:
            best = best1
            best_x = best_x1
            best_y = best_y1

        result["outputs"] += [{"HedgePositionName": best, "OptimalHedgeRatio": round(best_x, 3), "NumFuturesContract": round(best_y)}]


    logging.info("My result :{}".format(result))
    return json.dumps(result)
