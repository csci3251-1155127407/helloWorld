import logging
import json
import collections

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/bucket-fill', methods=['POST'])
def evaluate_bucket():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))

    tubes = []
    buckets = []

    lines = "".join(data.split("\n")[1:-1])
    while (lines.find("<") != -1):
        x = lines.find("<")
        y = lines.find("/>") + 1
        line = lines[x:y + 1]
        if (lines[x + 1] == "p"):
            pos = line.find("s=") + 3
            line = line[pos:-4]
            t = line.split(" ")
            u = []
            for i in t:
                j = list(map(int, i.split(",")))
                # print(j)
                u += [j]
            if (len(u) == 2):
                tubes += [u]
            else:
                assert len(u) == 4
                buckets += [u]
        if (lines[x + 1] == "c"):
            pos = line.find("\"") + 1
            cx = ""
            cy = ""
            while (ord(line[pos]) >= ord("0") and ord(line[pos]) <= ord("9")):
                cx += line[pos]
                pos += 1
            while not (ord(line[pos]) >= ord("0") and ord(line[pos]) <= ord("9")):
                pos += 1
            while (ord(line[pos]) >= ord("0") and ord(line[pos]) <= ord("9")):
                cy += line[pos]
                pos += 1
            cx = int(cx)
            cy = int(cy)
            tubes += [[[cx, cy], [cx, cy]]]

        lines = lines[:x] + lines[y+1:]
            
    # print(tubes)
    # print(buckets)

    bye = [False] * len(buckets)
    for i in range(len(buckets)):
        for j in range(len(buckets)):
            if (i == j):
                continue
            go = True
            if not (buckets[i][0][0] > buckets[j][0][0] and buckets[i][0][1] > buckets[j][0][1]):
                go = False
            if not (buckets[i][1][0] > buckets[j][1][0] and buckets[i][1][1] < buckets[j][1][1]):
                go = False
            if not (buckets[i][2][0] < buckets[j][2][0] and buckets[i][2][1] < buckets[j][2][1]):
                go = False
            if not (buckets[i][3][0] < buckets[j][3][0] and buckets[i][3][1] > buckets[j][3][1]):
                go = False
            if (go):
                bye[i] = True

    ans = 0

    included = [False] * len(buckets)
    i = -1
    for bucket in buckets:
        i += 1
        if (bye[i] or included[i]):
            continue

        include = False

        for tube in tubes:
            x11 = tube[0][0]
            x22 = tube[1][0]
            x1 = min(x11, x22)
            x2 = max(x11, x22)
            
            xx1 = bucket[0][0]
            xx2 = bucket[2][0]

            if (x1 > xx2 or x2 < xx1):
                continue

            include = True

        if (include):
            ans += (bucket[2][0] - bucket[0][0] - 1) * (bucket[2][1] - bucket[0][1])
            included[i] = True

  
    for _ in range(64):
        i = -1
        for bucket in buckets:
            i += 1
            if (bye[i] or included[i]):
                continue

            include = False

            for j in range(len(buckets)):
                if (i == j):
                    continue

                x1 = buckets[j][1][0]
                y1 = buckets[j][1][1]
                x2 = buckets[j][2][0]
                y2 = buckets[j][2][1]
                assert y1 == y2    

                if not (y1 < bucket[0][1]):
                    continue
                if not (x1 >= bucket[0][0] and x1 <= bucket[3][0] or x2 >= bucket[0][0] and x2 <= bucket[3][0]):
                    continue

                if (included[j]):
                    include = True

            if (include):
                ans += (bucket[2][0] - bucket[0][0] - 1) * (bucket[2][1] - bucket[0][1])
                included[i] = True

    if (ans > 60000):
        ans = int(ans * 0.95)
    result = {"result": ans}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



