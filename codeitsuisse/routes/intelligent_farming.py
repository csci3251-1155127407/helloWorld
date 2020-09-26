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

    for test in tests:
        result["list"] += [{"id": test["id"]}]
        s = test["geneSequence"]

        cnt_a = cnt_c = cnt_g = cnt_t = 0
        for ch in s:
            if (ch == 'A'):
                cnt_a += 1
            if (ch == 'C'):
                cnt_c += 1
            if (ch == 'G'):
                cnt_g += 1
            if (ch == 'T'):
                cnt_t += 1

        print(cnt_c)
        num_cc = 0
        num_acgt = 0
        max_score = 0
        for i in range(cnt_c // 2 + 1):
            print("i =", i)
            cnt_acgt = min(cnt_a, cnt_c - i * 2, cnt_g, cnt_t)
            for j in range(cnt_acgt + 1):
                score_cc = i * 25
                score_acgt = j * 15
                
                rem_a = cnt_a - j
                rem_c = cnt_c - i * 2 - j
                rem_g = cnt_g - j
                rem_t = cnt_t - j

                rem_a -= i * 2
                rem_a -= j
                rem_a -= (rem_c + rem_g + rem_t) * 2
                rem_a = max(0, rem_a)

                score_aaa = rem_a // 3 * 20

                if (score_cc + score_acgt - score_aaa > max_score):
                    max_score = score_cc + score_acgt - score_aaa
                    num_cc = i
                    num_acgt = j

        rem_a = cnt_a - num_acgt
        rem_c = cnt_c - num_cc * 2 - num_acgt
        rem_g = cnt_g - num_acgt
        rem_t = cnt_t - num_acgt

        # ans = "ACGT" * num_acgt

        for i in range(num_acgt):
            if (rem_a >= 1):
                ans += "A"
                rem_a -= 1
            ans += "ACGT"

        for i in range(num_cc):
            if (rem_a >= 2):
                ans += "AA"
                rem_a -= 2
            ans += "CC"

        for i in range(rem_c):
            if (rem_a >= 2):
                ans += "AA"
                rem_a -= 2
            ans += "C"

        for i in range(rem_g):
            if (rem_a >= 2):
                ans += "AA"
                rem_a -= 2
            ans += "G"

        for i in range(rem_t):
            if (rem_a >= 2):
                ans += "AA"
                rem_a -= 2
            ans += "T"

        ans += "A" * rem_a

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

        result["list"][-1]["geneSequence"] = ans

        print(max_score)

    logging.info("My result :{}".format(result))
    return jsonify(result)



