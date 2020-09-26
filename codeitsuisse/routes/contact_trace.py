import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def diff(s, t):
    assert len(s) == len(t)

    res = 0
    first = 0
    for i in range(len(s)):
        if (s[i] != t[i]):
            res += 1
            if (i == 0 or s[i - 1] == "-"):
                first += 1
                
    if (res >= 3):
        return 0 # no
    if (first <= 1):
        return 1 # silent
    assert first == 2
    return 2 # non-silent

def dfs():
    global data
    global vis
    global so_far
    global ans
    if (len(so_far) > 1 and so_far[-1][1] == data["origin"]["genome"]):
        # print("so_far:", so_far)
        ans += [so_far[:]]
        # print("ans:", ans)
        return
    
    for i in range(len(data["cluster"])):
        if (vis[i] == 1):
            continue
        if (diff(so_far[-1][1], data["cluster"][i]["genome"]) == 0):
            continue
        vis[i] = 1
        so_far += [(data["cluster"][i]["name"], data["cluster"][i]["genome"])]
        dfs()
        vis[i] = 0
        so_far.pop()
    if (diff(so_far[-1][1], data["origin"]["genome"]) != 0):
        so_far += [(data["origin"]["name"], data["origin"]["genome"])]
        dfs()
        so_far.pop()


@app.route('/contact_trace', methods=['POST'])
def evaluate_contact_trace():
    global data
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    global vis
    vis = [0] * len(data["cluster"])
    global ans
    ans = []
    global so_far
    so_far = []

    so_far += [(data["infected"]["name"], data["infected"]["genome"])]
    dfs()

    # print("ans:", ans)

    result = []
    for i in ans:
        t = [j[0] for j in i]
        # print("t:", t)
        for j in range(len(i) - 1):
            if (diff(i[j][1], i[j + 1][1]) == 2):
                t[j] += "*"
        result += [" -> ".join(t)]

    if (len(result) == 0):
        print("=" * 88)

    logging.info("My result :{}".format(result))
    return json.dumps(result)
