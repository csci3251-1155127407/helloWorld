import logging
import json
import wordninja

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def rot(s, n):
    t = [s[i] for i in range(len(s))]
    for i in range(len(t)):
        t[i] = chr((ord(t[i]) - ord("a") + n) % 26 + ord("a"))
    t = "".join(t)
    return t

def long_num_palin(s):
    res1, res2, res3 = 0, 0, ""
    for i in range(len(s)):
        # print(i, end=" ")
        j = 0
        while (i - (j + 1) >= 0 and i + (j + 1) < len(s) and s[i - (j + 1)] == s[i + (j + 1)]):
            j += 1
            res2 += 1
        # print(j)
        if (j * 2 + 1 > res1):
            res1 = j * 2 + 1
            res3 = s[i - j:i + j + 1]
    return res1, res2, res3

# long_num_palin("racecarisanenglishpalindrome")

def transform(s):
    res1, res2, res3 = long_num_palin(s)
    return rot(s, res2 + sum(ord(ch) for ch in res3))

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = [{"id": i["id"], "encryptionCount": 0, "originalText": ""} for i in data]

    test = [i["encryptedText"] for i in data]

    # from codeitsuisse.bored_scribe_py import ANS

    ANS = []
    for s in test:
        num_words = [0] * 26
        mn = 0
        for i in range(26):
            t = rot(s, i)
            num_words[i] = len(wordninja.split(t))
            if (num_words[i] < num_words[mn]):
                mn = i

        ANS += [" ".join(wordninja.split(rot(s, mn)))]

    print(1)

    for i in range(len(ANS)):
        result[i]["originalText"] = ANS[i]

    print(ANS)

    for i in range(len(test)):
        f = "".join(ANS[i].split(" "))
        cnt = 0
        while (test[i] != f):
            f = transform(f)
            cnt += 1
        result[i]["encryptionCount"] = cnt

    print(3)

    logging.info("My result :{}".format(result))
    return json.dumps(result);



