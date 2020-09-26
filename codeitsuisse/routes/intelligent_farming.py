import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluate_intelligent_farming():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    result = {"runId": data["runId"], "list": []}
    tests = data["list"]

    max_len = 0

    for test in tests:
        result["list"] += [{"id": test["id"]}]
        s = test["geneSequence"]
        max_len = max(max_len, len(s))


        # cnt_a = cnt_c = cnt_g = cnt_t = 0
        # for ch in s:
        #     if (ch == 'A'):
        #         cnt_a += 1
        #     if (ch == 'C'):
        #         cnt_c += 1
        #     if (ch == 'G'):
        #         cnt_g += 1
        #     if (ch == 'T'):
        #         cnt_t += 1

        # num_cc = 0
        # max_score = 0
        # for i in range(cnt_c // 2):
        #     score = i * 25
        #     score += min(cnt_a, cnt_c - i * 2, cnt_g, cnt_t) * 15
        #     if (score > max_score):
        #         max_score = score
        #         num_cc = i

        # num_acgt = min(cnt_a, cnt_c - num_cc * 2, cnt_g, cnt_t)
        # num_a = cnt_a - num_acgt

        # ans = "ACGT" * num_acgt
        # for i in range(num_cc):
        #     if (num_a >= 2):
        #         num_a -= 2
        #         ans += "AA"
        #     ans += "CC"

        # for i in range(num_a):
        #     ans += "A"

        # ans += "A" * num_a
        # result["list"][-1]["geneSequence"] = ans

    print(max_len)

    logging.info("My result :{}".format(result))
    return json.dumps(result)



