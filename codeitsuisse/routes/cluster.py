import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

DX = [-1, -1, -1, 0, 0, 1, 1, 1]
DY = [-1, 0, 1, -1, 1, -1, 0, 1]
D = len(DX)

def dfs(x, y):
    if (x < 0 or x >= r or y < 0 or y >= c):
        return
    if (data[x][y] == "*"):
        return
    data[x][y] = "*"

    for i in range(D):
        dfs(x + DX[i], y + DY[i])



@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    global data
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    global r, c
    r, c = len(data), len(data[0])

    ans = 0
    for i in range(r):
        for j in range(c):
            if (data[i][j] == "1"):
                ans += 1
                dfs(i, j)

    result = {"answer": ans}

    logging.info("My result :{}".format(result))
    return json.dumps(result)



