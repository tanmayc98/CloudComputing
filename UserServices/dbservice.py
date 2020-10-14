import pymysql
import json
import os

env = os.environ

pw = env.get("dbpw", None)

c_info = {
    "host": "ec2rdbuserservice.ceavmztkucmk.us-east-2.rds.amazonaws.com",
    "user": "dbuser",
    "password": pw,
    "cursorclass": pymysql.cursors.DictCursor
}

conn = pymysql.connect(**c_info)
cur = conn.cursor()
res = cur.execute("show databases;")
res = cur.fetchall()

print("database = {}".format(json.dumps(res, indent=4, default=str)))
