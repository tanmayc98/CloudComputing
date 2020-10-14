import os


def get_connect_info():
    env = os.environ

    keys = ["aws_access_key_id", "aws_secret_access_key", "region_name"]
    result = {}

    for k in keys:
        result[k] = env.get(k, None)

    return result


# print("Connect info = {}".format(get_connect_info()))
