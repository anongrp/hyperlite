""" Parser module help to parse hyperql query language to an plan python object """

import re

class QueryOperations:
    @staticmethod
    def equal_to(data, field):
        return data == field

    @staticmethod
    def not_equal_to(data, field):
        return data != field

    @staticmethod
    def graeter_than(data, field):
        return data > field

    @staticmethod
    def less_than(data, field):
        return data < field

    @staticmethod
    def graeter_than_equal(data, field):
        return data >= field

    @staticmethod
    def less_than_equal(data, field):
        return data <= field

    @staticmethod
    def and_operation(data, field):
        return data and field

    @staticmethod
    def or_operation(data, field):
        return data or field

    @staticmethod
    def not_operation(field):
        return not field

    @staticmethod
    def echo(field):
        return field

    @staticmethod
    def get_from_command(cmd):
        operations = {
            "&eq": QueryOperations.equal_to,
            "&neq": QueryOperations.not_equal_to,
            "&gt": QueryOperations.graeter_than,
            "&lt": QueryOperations.less_than,
            "&gte": QueryOperations.graeter_than_equal,
            "&lte": QueryOperations.less_than_equal,
            "__it": QueryOperations.echo
        }
        return operations.get(cmd)


class Query :
    def __init__(self):
        self.required_field = []
        self.needed_query_methods = []
    

def hyperql_parser(query: str) -> Query:

    query_obj = Query()
    query_instractions = []

    # For removing the white spaces
    space_pattern = re.compile(r'\s+')
    
    def get_field_name(raw_query):
        if raw_query.find('=') > -1:
            return raw_query[0 : raw_query.find("=")].strip()
        else:
            return raw_query[0 : raw_query.find("&")].strip()

    def get_filter(raw_query):
        if raw_query.find('__it') > -1:
            return QueryOperations.get_from_command("__it")
        else:
            cmd = raw_query[raw_query.find("&") : raw_query.find(" ", raw_query.find("&"))]
            return QueryOperations.get_from_command(cmd)

    def parse_filters(raw_query):
        field = get_field_name(raw_query)
        filter = get_filter(raw_query)
        query_obj.needed_query_methods.append({
            "field": field,
            "filter": filter
        })

    for instraction in query.strip().split(","):
        query_instractions.append(instraction.strip())
    
    for raw_query in query_instractions:
        if raw_query.find("=") > -1:
            query_obj.required_field.append(get_field_name(raw_query))
        
        parse_filters(raw_query)

    return query_obj



if __name__ == "__main__":
    query = """ 
            name = __it, 
            age = __it, 
            city &eq "city_name"
            """
    obj = hyperql_parser(query)

    print(obj.needed_query_methods)