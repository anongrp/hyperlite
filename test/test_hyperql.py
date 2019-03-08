import unittest
from hyperql import parser


class TestHyperQl(unittest.TestCase):

    def testViewQuery(self):
        query = """
        name, email,
        age &eq 18
        """
        view = ["name", "email"]
        query_obj = parser.parser(query)
        self.assertEqual(query_obj.view, view)

    def testSelectiveQuery(self):
        query = """
                name, email,
                age &eq 18
                """
        field = 'age'
        query_obj = parser.parser(query)
        self.assertEqual(query_obj.selective[0]['field'], field)
