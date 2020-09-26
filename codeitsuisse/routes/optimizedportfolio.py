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
    return x

def calcContract(index_future):
    y = calcRatio(index_future) * portfolio["Value"] / (index_future["IndexFuturePrice"] * index_future["Notional"])
    return y

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

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

        lowestRatio = 0
        lowestFuture = 0

        for i in range(len(index_futures)):
            x = calcRatio(index_futures[i])
            y = calcContract(index_futures[i])
            z = index_futures[i]["FuturePrcVol"]

            print(F"WTF x: {x}, y: {y}, z: {z}")
            if (calcRatio(index_futures[i]) < calcRatio(index_futures[lowestRatio])) or ((calcRatio(index_futures[i]) == calcRatio(index_futures[lowestRatio]) and calcContract(index_futures[i]) < calcContract(index_futures[lowestRatio]))):
                lowestRatio = i
            if (index_futures[i]["FuturePrcVol"] < index_futures[lowestFuture]["FuturePrcVol"]) or (index_futures[i]["FuturePrcVol"] == index_futures[lowestFuture]["FuturePrcVol"] and calcContract(index_futures[i]) < calcContract(index_futures[lowestFuture])):
                lowestFuture = i

        if calcContract(index_futures[lowestRatio]) < calcContract(index_futures[lowestFuture]):
            ans = lowestRatio
        else:
            ans = lowestFuture

        result["outputs"] += [{"HedgePositionName": index_futures[ans]["Name"], "OptimalHedgeRatio": round_up(calcRatio(index_futures[ans]), 3), "NumFuturesContract": int(round_up(calcContract(index_futures[ans]), 0))}]


    logging.info("My result :{}".format(result))
    return json.dumps(result)
