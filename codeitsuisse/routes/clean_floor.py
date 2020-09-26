import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

a = []

def fix(index):
    if (a[index] < 0):
        a[index] %= 2
        a[index] = abs(a[index])

def deal_with(index):
    a[index + 1] -= a[index]
    fix(index + 1)
    return a[index] * 2


@app.route('/clean_floor', methods=['POST'])
def evaluate_clean_floor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data['tests']

    result = {}
    result['answers'] = {}

    for test_id in tests:
        test = tests[str(test_id)]
        global a
        a = test['floor']

        print(a)
        assert len(a) > 1
        
        last_dirty = 0
        for i in range(len(a)):
            if (a[i] > 0):
                last_dirty = i

        ans = 0
        for i in range(last_dirty):
            res = deal_with(i)
            print(res)
            ans += res
            if (a[last_dirty] == 0):
                break
            a[i + 1] -= 1
            fix(i + 1)
            ans += 1
        last_dirty_level = a[last_dirty]
        ans += last_dirty_level + (last_dirty_level + 1) * last_dirty_level

        result['answers'][str(test_id)] = ans

    logging.info("My result :{}".format(result))
    return json.dumps(result)



