import pymysql
import json
import os


class UserService:
    # Again, this would not be hardcoded and would come from the configuration/environment.

    env = os.environ

    # pw = env.get("dbpw", None)
    pw = "dbuserdbuser"

    __c_info = {
        "host": "ec2rdbuserservice.ceavmztkucmk.us-east-2.rds.amazonaws.com",
        "user": "dbuser",
        "password": pw,
        "cursorclass": pymysql.cursors.DictCursor
    }

    __table_name = "users"

    def __init__(self):
        self.table_name = UserService.__table_name
        self.c_info = UserService.__c_info

    def fetch_all(self):
        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        res = cur.execute("show databases;")
        res = cur.fetchall()

        conn.close()

        return res

    def query(self, query_params):

        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        if query_params is not None:
            if "limit" in query_params.keys():
                query_limit = int(query_params["limit"])
            else:
                query_limit = 10000

            if "offset" in query_params.keys():
                query_offset = int(query_params["offset"])
            else:
                query_offset = 0

            if "last_name" in query_params.keys():
                query_last_name = query_params["last_name"]
            else:
                query_last_name = None
        else:
            query_limit = 10000
            query_offset = 0
            query_last_name = None

        if query_last_name is None:
            result = self.get_all(cur, query_limit, query_offset)
        else:
            result = self.get_by_last_name(cur, query_limit, query_offset, query_last_name)

        conn.close()

        return result

    def get_all(self, cur, query_limit, query_offset):

        q_run = "select * from user_schema.users limit {} offset {}".format(query_limit, query_offset)

        cur.execute(q_run)

        res = cur.fetchall()

        return res

    def get_by_last_name(self, cur, query_limit, query_offset, query_last_name):

        # q_run = "select * from user_schema.users where `last_name` = {} limit {} offset {}"\
        #     .format(query_last_name, query_limit, query_offset)

        q_run = "select * from user_schema.users where `last_name` = '{}'" \
            .format(query_last_name)

        cur.execute(q_run)

        res = cur.fetchall()

        return res

    def add(self, query_params):

        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        res = dict()

        if query_params is not None:
            if "last_name" in query_params.keys():
                insert_last_name = query_params["last_name"]
            else:
                insert_last_name = None

            if "first_name" in query_params.keys():
                insert_first_name = query_params["first_name"]
            else:
                insert_first_name = None

            if "email" in query_params.keys():
                insert_email = query_params["email"]
            else:
                insert_email = None

            if "hashed_password" in query_params.keys():
                insert_hashed_password = query_params["hashed_password"]
            else:
                insert_hashed_password = None

            if "status" in query_params.keys():
                insert_status = query_params["status"]
            else:
                insert_status = None

            if "created_date" in query_params.keys():
                insert_created_date = query_params["created_date"]
            else:
                insert_created_date = None

            q_run = "insert into user_schema.users\
                     (`last_name`, `first_name`, `email`, `hashed_password`, `status`, `created_date`)\
                     values ('{}', '{}', '{}', '{}', '{}', '{}')"\
                    .format(insert_last_name, insert_first_name, insert_email, insert_hashed_password, insert_status, \
                            insert_created_date)
            print(q_run)

            cur.execute(q_run)

            conn.commit()

            res["Response"] = "Inserted one user."

        else:
            res["Response"] = "ERROR: No input."

        conn.close()

        return res
