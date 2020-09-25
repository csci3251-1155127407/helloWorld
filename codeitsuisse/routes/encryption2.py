import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/encryption', methods=['POST'])
def evaluate_encryption():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = []
    print(data)
    for i in data:
        n = i["n"]
        text = list(i["text"])
        text = [j for j in text if j.isalnum()]
        ans = ["-"] * len(text)
        j = 0
        jj = 0
        for k in range(len(text)):
            ans[j] = text[k].upper()
            j += n
            if (j >= len(text)):
                jj += 1
                j = jj
        result += ["".join(ans)]

    logging.info("My result :{}".format(result))
    return json.dumps(result);



