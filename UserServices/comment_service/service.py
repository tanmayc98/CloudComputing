
#
# The service would use a factory or configuration to determine which implementation
# of BaseDataTable to get. I am not going to bother to do that and import the table
# for the backend that the service uses.
#
# https://en.wikipedia.org/wiki/Factory_method_pattern
#
from DataAccessLayer.DynamoDBDataTable import DynamoDBDataTable

class CommentService:
    """
    In some designs, this class would inherit from a base framework class for implementing services.

    Example of some REST/web application frameworks are at
    https://hub.packtpub.com/which-python-framework-is-best-for-building-restful-apis-django-or-flask/

    There are many, many frameworks for all languages and application servers.
    """

    # Again, this would not be hardcoded and would come from the configuration/environment.
    __table_name = "FantasyComments"

    def __init__(self):
        self._table_name = CommentService.__table_name
        self._data_table = DynamoDBDataTable(self._table_name, key_columns="comment_id")

    def get_by_comment_id(self, comment_id):

        result = self._data_table.find_by_primary_key(comment_id)
        return result

