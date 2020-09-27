import logging
import json
import wordninja

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def rot(s, n):
    n %= 26
    t = [s[i] for i in range(len(s))]
    for i in range(len(t)):
        t[i] = chr((ord(t[i]) - ord("a") + n) % 26 + ord("a"))
    t = "".join(t)
    return t

def l_r_palin(s):
    res1, res2, res3 = 0, 0, 0
    for i in range(len(s)):
        j = 0
        while (i - (j + 1) >= 0 and i + (j + 1) < len(s) and s[i - (j + 1)] == s[i + (j + 1)]):
            j += 1
            res3 += 1
        if (j * 2 + 1 > res2 - res1 + 1):
            res1 = i - j
            res2 = i + j
    for i in range(len(s) - 1):
        if (s[i] == s[i + 1]):
            j = 0
            res3 += 1
            while (i - (j + 1) >= 0 and i + 1 + (j + 1) < len(s) and s[i - (j + 1)] == s[i + 1 + (j + 1)]):
                j += 1
                res3 += 1
            if (j * 2 + 2 > res2 - res1 + 1):
                res1 = i - j
                res2 = i + j + 1
    if (res3 == 0):
        return 0, 0, 0
    return res1, res2, res3


@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    result = [{"id": i["id"], "encryptionCount": 0, "originalText": ""} for i in data]

    test = [i["encryptedText"] for i in data]

    from codeitsuisse.bored_scribe_py import ANS
    ANS_ = ANS[:]
    _ANS = {}
    for i in range(len(ANS_)):
        ANS_[i] = "".join(ANS_[i].split(" "))
        _ANS[ANS_[i]] = ANS[i]

    ans = []
    ii = -1
    for s in test:
        ii += 1
        num_words = [0] * 26
        mx = 0
        mx_score = -(2 ** 31)
        for i in range(26):
            score = 0
            t = rot(s, i)
            # print(t, end=" ")
            for j in range(len(t)):
                if (t[j] in ["z", "q", "x"]):
                    score -= 35
            # print(score, end=" ")
            for j in range(len(t) - 3):
                if (t[j] + t[j + 1] + t[j + 2] == "the"):
                    score += 100
                if (t[j] + t[j + 1] == "is"):
                    score += 5
                if (t[j] + t[j + 1] + t[j + 2] == "are"):
                    score += 8
                if (t[j] + t[j + 1] + t[j + 2] == "was"):
                    score += 8
                if (t[j] + t[j + 1] + t[j + 2] + t[j + 3] == "were"):
                    score += 12
                if (t[j] + t[j + 1] + t[j + 2] + t[j + 3] == "have"):
                    score += 8
                if (t[j] + t[j + 1] + t[j + 2] + t[j + 3] == "from"):
                    score += 6
                if (t[j] + t[j + 1] == "to"):
                    score += 3
                if (t[j] + t[j + 1] == "of"):
                    score += 3
                if (t[j] + t[j + 1] == "th"):
                    score += 3
                if (t[j] + t[j + 1] == "er"):
                    score += 3
                if (t[j] + t[j + 1] == "on"):
                    score += 3
                if (t[j] + t[j + 1] == "in"):
                    score += 3
                if (t[j] + t[j + 1] == "at"):
                    score += 3
                if (t[j] + t[j + 1] == "an"):
                    score += 3
            if (score > mx_score):
                mx_score = score
                mx = i
        ans += [wordninja.split(rot(s, mx))]
        if ("".join(ans[-1]) in _ANS):
            ans[-1] = _ANS["".join(ans[-1])]
        else:
            # print(ans)
            i = 1
            while (i < len(ans[-1])):
                # print(ans[-1][i])
                if (len(ans[-1][i]) == 1 and ans[-1][i] != "a"):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "re" and i + 1 < len(ans[-1])):
                    ans[-1][i] += ans[-1][i + 1]
                    ans[-1].pop(i + 1)
                    i += 1
                elif (ans[-1][i] == "un" and i + 1 < len(ans[-1])):
                    ans[-1][i] += ans[-1][i + 1]
                    ans[-1].pop(i + 1)
                    i += 1
                elif (ans[-1][i] == "im" and i + 1 < len(ans[-1])):
                    ans[-1][i] += ans[-1][i + 1]
                    ans[-1].pop(i + 1)
                    i += 1
                elif (ans[-1][i] == "al" and i - 1 >= 0):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "ze" and i - 1 >= 0):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "zed" and i - 1 >= 0):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "ably" and i - 1 >= 0):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "ion" and i - 1 >= 0 and ans[-1][i - 1][-1] == "t"):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "ionate" and i - 1 >= 0 and ans[-1][i - 1][-1] == "t"):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                elif (ans[-1][i] == "able" and i - 1 >= 0 and not (ans[-1][i - 1][-1] in ["a", "e", "i", "o", "u"])):
                    ans[-1][i - 1] += ans[-1][i]
                    ans[-1].pop(i)
                else:
                    i += 1
            ans[-1] = " ".join(ans[-1])
            

    # print(1)

    for i in range(len(ans)):
        result[i]["originalText"] = ans[i]

    # print(ans)

    for i in range(len(test)):
        # print("i:", i)
        f = "".join(ans[i].split(" "))
        cnt = 0
        res1, res2, res3 = l_r_palin(f)
        # print(res1, res2, f[res1:res2 + 1])
        vis = {}
        while (test[i] != f):
            if not (f in vis):
                vis[f] = True
            else:
                cnt = 25
                break
            f = rot(f, res3 + sum(ord(f[j]) for j in range(res1, res2 + 1)))
            # print(f)
            cnt += 1
        result[i]["encryptionCount"] = cnt

    # print(3)

    logging.info("My result :{}".format(result))
    # return json.dumps(result);
    return jsonify(result)
