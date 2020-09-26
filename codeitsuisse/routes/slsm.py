import logging
import json
import collections

from flask import request, jsonify;
from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/slsm', methods=['POST'])
def evaluate_slsm():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    n = data["boardSize"]
    m = data["players"]
    edges = data["jumps"]

    # to = [i for i in range(n + 1)]
    # spTo = [0 for i in range(n + 1)]
    # vis = [[0, 0, 0] for i in range(n + 1)]
    #
    # for edge in edges:
    #     x, y = list(map(int, edge.split(':')))
    #     print(x, y)
    #     if x == 0:
    #         spTo[y] = 1
    #     elif y == 0:
    #         spTo[x] = 2;
    #     else:
    #         to[x] = y
    #
    # que = collections.deque([])
    # que.append((1, 1, [], 0))
    # vis[1][0] = 1
    # winPath = []
    #
    # while len(que):
    #     current = que.popleft()
    #     if current[0] == n:
    #         winPath = current[2]
    #         break
    #
    #     currentPath = current[2]
    #     for i in range(1, 7):
    #         if current[3] == 2:
    #             nxt = current[0] - i
    #             path = currentPath + [-i]
    #         elif current[3] == 1:
    #             nxt = current[0] + i
    #             path = currentPath + [-i]
    #         else:
    #             nxt = current[0] + i
    #             path = currentPath + [i]
    #
    #         if nxt > n:
    #             nxt -= n
    #
    #         if spTo[nxt] == 0:
    #             st = 0
    #             nxt = to[nxt]
    #         elif spTo[nxt] == 1:
    #             st = 1
    #         else:
    #             st = 2
    #
    #         if vis[nxt][st]:
    #             continue
    #         vis[nxt][st] = 1
    #         if st == 0:
    #             que.append((nxt, current[1] + 1, path[:], st))
    #         else:
    #             que.appendleft((nxt, current[1], path[:], st))
    #
    # print(winPath)
    # realPath =

    result = []

    logging.info("My result :{}".format(result))
    return json.dumps(result);



