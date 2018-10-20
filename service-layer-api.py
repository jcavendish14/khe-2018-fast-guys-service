from flask import Flask, request
import flask
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='root',
    port=3306,
    db='khe2018'
)

@app.route("/numberOfRoutes")
def getNumRoutes():
    json_dict = {}
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM routes")
        rv = cursor.fetchall()
        num_routes = len(rv)
        json_dict['numberRoutes'] = num_routes

    return flask.jsonify(json_dict)

'''
Fetch a particular routeId from the database
@param routeId - an int representing the ID of the route
'''
@app.route("/getRoute/<routeId>")
def getRoute(routeId):
    json_dict = {}
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM routes WHERE routeId={}".format(routeId))
        rv = cursor.fetchone()
        json_dict = {
            'routeId': rv[0],
            'userId': rv[1],
            'distance': float(rv[3]),
            'city': rv[4],
            'state': rv[5],
            'rating': float(rv[6]),
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
        print(user_dict)
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
    offset = request.args.get('offset')
    response_len = request.args.get('length')
    return offset + ' ' + response_len