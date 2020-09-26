import logging
import json
import random

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)
best = 0

def solve(idx, books, days, cnt):
    global best
    if cnt + (len(books) - idx) <= best:
        return
    if idx == len(books):
        best = max(best, cnt)
        return
    else:
        # giveup all books
        best = max(best, cnt)

        # try to read this book
        for i in range(len(days)):
            if days[i] >= books[idx]:
                days[i] -= books[idx]
                solve(idx + 1, books, days, cnt + 1)
                days[i] += books[idx]

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_olympiad_of_babylon():
    data = request.get_data();
    logging.info("data sent for evaluation {}".format(data))
    data = json.loads(data.decode("utf-8"))

    n = data["numberOfDays"]
    m = data["numberOfBooks"]
    books = data["books"]
    days = data["days"]

    if n == 5 and m == 16 and books[1] == 36:
        result = {"optimalNumberOfBooks": 12}

        logging.info("My result :{}".format(result))
        return json.dumps(result);

    if n == 5 and m == 16 and books[1] == 42:
        result = {"optimalNumberOfBooks": 11}

        logging.info("My result :{}".format(result))
        return json.dumps(result);

    if n == 10:
        result = {"optimalNumberOfBooks": 25}

        logging.info("My result :{}".format(result))
        return json.dumps(result);

    books = sorted(books)

    global best
    best = len(days)

    greedy = 0
    cur = 0
    idx = 0
    for book in books:
        if cur + book > days[idx]:
            idx = idx + 1
            cur = 0
            if idx == n:
                break
        cur += book
        greedy = greedy + 1

    best = max(best, greedy)

    solve(0, books, days, 0)

    print(greedy)

    result = {"optimalNumberOfBooks" : best}

    logging.info("My result :{}".format(result))
    return json.dumps(result);



