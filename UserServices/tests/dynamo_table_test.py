
from DataAccessLayer.DynamoDBDataTable import DynamoDBDataTable as DynamoDBTable


def t1():
    t1 = DynamoDBTable("FantasyComments")
    print("t1 = ", t1)

def t2():
    t1 = DynamoDBTable("FantasyComments", key_columns="comment_id")
    res = t1.find_by_primary_key(key_fields="123")
    print("t2 result = ", res)


#t1()
t2()