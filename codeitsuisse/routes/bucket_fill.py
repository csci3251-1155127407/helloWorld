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
                print(j)
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
            
    print(tubes)
    print(buckets)

    ans = 0
    for bucket in buckets:
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

    result = {"result": ans}
    logging.info("My result :{}".format(result))
    return json.dumps(result);



