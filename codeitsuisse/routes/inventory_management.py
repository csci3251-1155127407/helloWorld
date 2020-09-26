import logging
import json

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)


def solve(word1, word2):
    len1, len2 = len(word1), len(word2)
    # Initialization
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
    dir = [[-1 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    # dir = 0, do nothing
    # dir = 1, add
    # dir = 2, remove
    # dir = 3, replace

    for i in range(len1 + 1):
        dp[i][0] = i
        dir[i][0] = 2

    for j in range(len2 + 1):
        dp[0][j] = j
        dir[0][j] = 1

    # Iteration
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if word1[i - 1].lower() == word2[j - 1].lower():
                dp[i][j] = dp[i - 1][j - 1]
                dir[i][j] = 0
            else:
                mn = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                if dp[i - 1][j] == mn:
                    dir[i][j] = 2
                elif dp[i][j - 1] == mn:
                    dir[i][j] = 1
                else:
                    dir[i][j] = 3

                dp[i][j] = mn + 1

    posx = len1
    posy = len2
    
    res_string = ""

    while posx > 0 or posy > 0:
        if dir[posx][posy] == 0:
            res_string += word1[posx - 1]
            posx = posx - 1
            posy = posy - 1
        elif dir[posx][posy] == 1:
            res_string += word2[posy - 1] + '+'
            posy = posy - 1
        elif dir[posx][posy] == 2:
            res_string += word1[posx - 1] + '-'
            posx = posx - 1
        else:
            res_string += word2[posy - 1]
            posx = posx - 1
            posy = posy - 1

    return (dp[len1][len2], word2, res_string[::-1], )

def cmp(x, y):
    if x[1] != y[1]:
        if x[1] < y[1]:
            return -1
        elif x[1] > x[1]:
            return 1
        else:
            return 0
    else:
        if x[2] < y[2]:
            return -1
        elif x[2] > x[2]:
            return 1
        else:
            return 0

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory_management():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = []

    for d in data:
        s = d.get('searchItemName')
        items = d.get('items')

        calc = sorted([solve(s, item) for item in items])[:10]
        result.append({"searchItemName" : s, "searchResult" : [e[2] for e in calc]})

    logging.info("My result :{}".format(result))
    return json.dumps(result);



