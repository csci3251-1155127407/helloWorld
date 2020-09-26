import logging
import json

from flask import request, jsonify;
from codeitsuisse import app;
from shapely.geometry import Polygon, LineString

logger = logging.getLogger(__name__)

def getExtrapoledLine(p1,p2):
    EXTRAPOL_RATIO = 1000000
    a = (p1[0]-EXTRAPOL_RATIO*(p2[0]-p1[0]), p1[1]-EXTRAPOL_RATIO*(p2[1]-p1[1]) )
    b = (p1[0]+EXTRAPOL_RATIO*(p2[0]-p1[0]), p1[1]+EXTRAPOL_RATIO*(p2[1]-p1[1]) )
    return LineString([a,b])

@app.route('/revisitgeometry', methods=['POST'])
def evaluate_revisitgeometry():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))

    shape = data.get("shapeCoordinates")
    shape_points = []

    for point in shape:
        shape_points.append((point['x'], point['y']))

    line = data.get("lineCoordinates")
    line_points = []

    for point in line:
        line_points.append((point['x'], point['y']))

    print(shape_points, line_points)

    if len(shape_points) == 2:
        polygon = LineString(shape_points)
    else:
        polygon = Polygon(shape_points)

    line = getExtrapoledLine(*line_points)
    print(line)
    intersect = list(line.intersection(polygon).coords)
    result = []

    for pair in intersect:
        result.append({"x" : pair[0], "y" : pair[1]})

    logging.info("My result :{}".format(result))
    return json.dumps(result);



