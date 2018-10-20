from flask import Flask
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='root',
    port=3306,
    db='khe2018'
)

@app.route("/<routeId>")
def getRoute(routeId):
    return routeId