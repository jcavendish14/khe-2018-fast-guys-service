from flask import Flask, request, send_file
import flask
from flask_cors import CORS
import pymysql
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/numberOfRoutes")
def getNumRoutes():
    conn = pymysql.connect(
        host='sql178.main-hosting.eu',
        user='u921505615_fg',
        passwd='password',
        port=3306,
        db='u921505615_khe18'
    )
    json_dict = {}
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM routes")
        rv = cursor.fetchall()
        num_routes = len(rv)
        json_dict['numberRoutes'] = num_routes
        print(json_dict)
    return flask.jsonify(json_dict)

'''
Fetch a particular routeId from the database
@param routeId - an int representing the ID of the route
'''
@app.route("/getRoute/<routeId>")
def getRoute(routeId):
    conn = pymysql.connect(
        host='sql178.main-hosting.eu',
        user='u921505615_fg',
        passwd='password',
        port=3306,
        db='u921505615_khe18'
    )
    json_dict = {}
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM routes WHERE routeId={}".format(routeId))
        rv = cursor.fetchone()
        json_dict = {
            'routeId': rv[0],
            'userId': rv[1],
            'kmlFile': rv[2],
            'distance': float(rv[3]),
            'city': rv[4],
            'state': rv[5],
            'rating': float(rv[6]),
            'snapshotFile': rv[7],
            'description': rv[8]
        }

    user_dict = {}
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE userId={}".format(json_dict['userId']))
        user_rv = cursor.fetchone()
        user_dict['userId'] = user_rv[0]
        user_dict['firstName'] = user_rv[1]
        user_dict['lastName'] = user_rv[2]
        user_dict['userName'] = user_rv[3]
        user_dict['city'] = user_rv[6]
        user_dict['state'] = user_rv[7]
        json_dict['user'] = user_dict

    comment_arr = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM comments WHERE routeId={}".format(routeId))
        comment_rv = cursor.fetchall()
        comment_dict = {}
        for res in comment_rv:
            cursor.execute("SELECT * FROM users WHERE userId={}".format(res[1]))
            user_data = cursor.fetchone()
            comment_dict['commentId'] = res[0]
            comment_dict['userId'] = res[1]
            comment_dict['routeId'] = res[2]
            comment_dict['text'] = res[3]
            comment_dict['username'] = user_data[3]
            comment_arr.append(comment_dict)
        json_dict['comments'] = comment_arr
		

    return flask.jsonify(json_dict)

@app.route("/getHomePage")
def getHomePageRoutes():
    conn = pymysql.connect(
        host='sql178.main-hosting.eu',
        user='u921505615_fg',
        passwd='password',
        port=3306,
        db='u921505615_khe18'
    )
    offset = request.args.get('offset', type=int)
    response_len = request.args.get('length', type=int)
    json_arr = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM routes LIMIT {} OFFSET {}".format(response_len, offset * response_len))
        rv = cursor.fetchall()
        for res in rv:
            cursor.execute("SELECT username FROM users WHERE userId={}".format(res[1]))
            username = cursor.fetchone()[0]
            json_dict = {
                'routeId': res[0],
                'userId': res[1],
                'kmlFile': res[2],
                'distance': float(res[3]),
                'city': res[4],
                'state': res[5],
                'rating': float(res[6]),
                'snapshotFile': res[7],
                'description': res[8],
                'username': username
            }
            json_arr.append(json_dict)

    return flask.jsonify(json_arr)

@app.route("/getFile/<routeId>")
def getFile(routeId):
    conn = pymysql.connect(
        host='sql178.main-hosting.eu',
        user='u921505615_fg',
        passwd='password',
        port=3306,
        db='u921505615_khe18'
    )
    file_type = request.args.get('type', type=str)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM routes WHERE routeId={}".format(routeId))
        rv = cursor.fetchone()
        if file_type == 'kml':
            return flask.jsonify({'fileName': rv[2]})
        elif file_type == 'jpg':
            return flask.jsonify({'fileName': rv[7]})
        else:
            return flask.jsonify({'err': 'no .{} file available'.format(file_type)})