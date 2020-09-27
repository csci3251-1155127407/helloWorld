import logging
import json
import collections

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluate_super():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests");

    result = {"answer" : {}}

    dirx = [0, 0, 1, -1]
    diry = [1, -1, 0, 0]

    for test in tests:
        maze = tests[test]["maze"]
        start = tests[test]["start"]
        end = tests[test]["end"]

        n = len(maze)
        m = len(maze[0])
        vis = [[0 for _ in range(m)] for _ in range(n)]
        que = collections.deque([])
        que.append((start[1], start[0], 1))
        vis[start[0]][start[1]] = 1

        res = -1

        while len(que):
            front = que.popleft()
            print(front[0], front[1])
            if front[0] == end[1] and front[1] == end[0]:
                res = front[2]
                break

            for i in range(4):
                dx = front[0] + dirx[i]
                dy = front[1] + diry[i]
                if dx < 0 or dx >= n or dy < 0 or dy >= m or maze[dx][dy] == 1 or vis[dx][dy] == 1:
                    continue
                vis[dx][dy] = 1
                que.append((dx, dy, front[2] + 1))

        result["answer"][test] = res

    logging.info("My result :{}".format(result))
    return json.dumps(result);



