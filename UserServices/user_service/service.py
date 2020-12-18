import pymysql
import json
import os
from utilities.authentication import get_token


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
            query_results = self.get_all(cur, query_limit, query_offset)
            result = dict()
            result["data"] = []
            result["links"] = []
            for q_res in query_results:
                temp_dict = {"links": []}
                temp_dict["links"].append({"rel": "user", "href": "/api/users/{}".format(q_res["id"])})
                temp_dict["data"] = q_res
                result["data"].append(temp_dict)
            result["links"].append({"rel": "self",
                                    "href": "https://localhost:8080/api/users?limit={}&offset={}".format(query_limit, query_offset)})
            if (query_offset - query_limit) >= 0:
                result["links"].append({"rel": "prev",
                                        "href": "https://localhost:8080/api/users?limit={}&offset={}".format(query_limit, query_offset - query_limit)})
            else:
                result["links"].append({"rel": "prev",
                                        "href": "https://localhost:8080/api/users?limit={}&offset={}".format(query_limit, 0)})
            if len(query_results) > 0:
                result["links"].append({"rel": "next",
                                        "href": "https://localhost:8080/api/users?limit={}&offset={}".format(query_limit, query_offset + query_limit)})
            else:
                result["links"].append({"rel": "next",
                                        "href": "https://localhost:8080/api/users?limit={}&offset={}".format(query_limit, query_offset)})
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

            if "password" in query_params.keys():
                input_password = {"password": str(query_params["password"])}
                token = get_token(input_password)
                insert_hashed_password = token.decode("UTF-8")
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

    def get_by_user_id(self, user_id):

        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        q_run = "select * from user_schema.users where `id` = '{}'" \
            .format(user_id)

        cur.execute(q_run)

        res = cur.fetchall()

        conn.close()

        return res

    def delete_by_user_id(self, user_id):

        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        res = dict()

        q_run = "delete from user_schema.users where `id` = '{}'" \
            .format(user_id)

        cur.execute(q_run)

        conn.commit()

        conn.close()

        res["Response"] = "Deleted user with id = {}.".format(user_id)

        return res

    def update_by_user_id(self, user_id, query_params):

        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        for key in query_params.keys():
            content = query_params[key]

            q_run = "update user_schema.users SET `{}` = '{}' where `id` = '{}'" \
                .format(key, content, user_id)

            cur.execute(q_run)

            conn.commit()

        q_run = "select * from user_schema.users where `id` = '{}'" \
            .format(user_id)

        cur.execute(q_run)

        res = cur.fetchall()

        conn.close()

        return res

    def verify(self, email, hashed_password):

        conn = pymysql.connect(**self.c_info)
        cur = conn.cursor()

        q_run = "select * from user_schema.users where `email` = '{}' and `hashed_password` = '{}'" \
            .format(email, str(hashed_password[:45]))

        cur.execute(q_run)

        res = cur.fetchall()

        conn.close()

        if len(res) > 0:
            return True, res
        else:
            return False, None
