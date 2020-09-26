import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def calc(index_future):
    global portfolio
    global index_futures
    x = portfolio["SpotPrcVol"] * index_future["CoRelationCoefficient"] / index_future["FuturePrcVol"]
    x = round(x, 3)
    y = x * portfolio["Value"] / (index_future["IndexFuturePrice"] * index_future["Notional"])

    # x = max(x, 0)
    # x = min(x, 1)

    return x, y

def calcRatio(index_future):
    x = portfolio["SpotPrcVol"] * index_future["CoRelationCoefficient"] / index_future["FuturePrcVol"]
    return my_round(x, 3)

def calcContract(index_future):
    y = calcRatio(index_future) * portfolio["Value"] / (index_future["IndexFuturePrice"] * index_future["Notional"])
    return my_round(y, 0)

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

def my_round(n, places):
    if places == 0:
        return int(normal_round((10 ** places) * n) / (10**places))
    else:
        return normal_round((10 ** places) * n) / (10**places)

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

        best = 0

        for i in range(len(index_futures)):
            x = calcRatio(index_futures[i])
            y = calcContract(index_futures[i])
            z = index_futures[i]["FuturePrcVol"]

            print(F"WTF x: {x}, y: {y}, z: {z}")

            if x <= calcRatio(index_futures[best]) and z <= index_futures[best]["FuturePrcVol"]:
                best = i
            elif x <= calcRatio(index_futures[best]) and z >= index_futures[best]["FuturePrcVol"] and y <= calcContract(index_futures[best]):
                best = i
            elif x >= calcRatio(index_futures[best]) and z <= index_futures[best]["FuturePrcVol"] and y <= calcContract(index_futures[best]):
                best = i

        print('BEST', best)

        ans = best

        result["outputs"] += [{"HedgePositionName": index_futures[ans]["Name"], "OptimalHedgeRatio": calcRatio(index_futures[ans]), "NumFuturesContract": calcContract(index_futures[ans])}]

    print(my_round(2.5, 0), my_round(3.5, 0), my_round(4.49, 0))
    logging.info("My result :{}".format(result))
    return json.dumps(result)
