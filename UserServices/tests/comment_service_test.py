
#
# The test programs would be in a separate package in real implementations.
#

from comment_service.service import CommentService


def t1():
    cs = CommentService()
    print("t1: Comment Service = ", cs)


def t2():
    cs = CommentService()
    res = cs.get_by_comment_id("123")
    print("t2: result = ", res)



#t1()
t2()