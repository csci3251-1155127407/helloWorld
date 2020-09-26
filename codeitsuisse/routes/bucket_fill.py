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

    lines = data.split("\n")
    for line in lines:
        if (line.find("polyline") != -1):
            pos = line.find("s=") + 3
            line = line[pos:-4]
            t = line.split(" ")
            u = []
            for i in t:
                j = list(map(int, i.split(",")))
                u += [j]
            if (len(u) == 2):
                tubes += [u]
            else:
                assert len(u) == 4
                buckets += [u]

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



