import logging
import json

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = []

    # for d in data:
    #     s = d.get('searchItemName')
    #     items = d.get('items')
    #
    #     calc = sorted([solve(s, item) for item in items])[:10]
    #     result.append({"searchItemName" : s, "searchResult" : [e[2] for e in calc]})

    logging.info("My result :{}".format(result))
    return json.dumps(result);



