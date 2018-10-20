from flask import Flask
from flask_cors import CORS
import MySQLdb

app = Flask(__name__)
CORS(app)

conn = MySQLdb.connect(
    host='127.0.0.1',
    user='root',
    passwd='root',
    port=3306,
    db='khe2018'
)

@app.route("/<routeId>")
def getRoute(routeId):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routes")
    return cursor.fetchOne()