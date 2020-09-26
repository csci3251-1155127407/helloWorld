import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluate_social_distancing():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");

    result = {"answers" : {}}
    for key in tests:
        seats = tests[key]["seats"]
        people = tests[key]["people"]
        spaces = tests[key]["spaces"]

        dp = [[0 for _ in range(people + 1)] for _ in range(seats + 1)]

        for i in range(0, seats + 1):
            dp[i][0] = 1

        for i in range(1, seats + 1):
            for j in range(1, people + 1):
                dp[i][j] = dp[i - 1][j]
                if j == 1:
                    dp[i][j] += dp[i - 1][j - 1]
                elif i - spaces - 1 >= 1:
                    dp[i][j] += dp[i - spaces - 1][j - 1]

        result["answers"][key] = dp[seats][people]


    logging.info("My result :{}".format(result))
    return json.dumps(result);



