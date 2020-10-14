import utilities.dynamodb as db

table = db.dynamodb.Table('FantasyComments')
print("Table = ", table, "\n")

it = db.get_item("FantasyComments", {"comment_id": "123"})
print("Item = ", it)

#x = get_item("BaseballComments",
#         key_value={"comment_id": "033b2839-0f16-40a5-9f5e-bf1d01b149d2"})

#print("Found comment  = ", x)

""""
response = do_a_scan('BaseballComments', None)
print("Scanning everything returns = ", json.dumps(response, indent=2, default=str))

print("\n")
FilterExpression=Attr("version_no").eq("2")
print("Filter = ", FilterExpression)
response = do_a_scan('BaseballComments',
                     filterexpression=Attr("labels").contains("USMC"))

print("Looking for something specific returns ", json.dumps(response, indent=2, default=str))
"""