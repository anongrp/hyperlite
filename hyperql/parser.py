""" Parser module help to parse hyperql query language to an plan python object """


class QueryOperations:
    @staticmethod
    def equal_to(data, field):
        return data == field

    @staticmethod
    def not_equal_to(data, field):
        return data != field

    @staticmethod
    def greater_than(data, field):
        return data < field

    @staticmethod
    def less_than(data, field):
        return data > field

    @staticmethod
    def greater_than_equal(data, field):
        return data <= field

    @staticmethod
    def less_than_equal(data, field):
        return data >= field

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
            "&gt": QueryOperations.greater_than,
            "&lt": QueryOperations.less_than,
            "&gte": QueryOperations.greater_than_equal,
            "&lte": QueryOperations.less_than_equal,
            "it": QueryOperations.echo
        }
        return operations.get(cmd)


class Query:
    def __init__(self):
        self.required_field = []
        self.needed_query_methods = []


def hyperql_parser(query: str) -> Query:
    query_obj = Query()
    query_instructions = []

    def get_field_name(raw_query):
        if raw_query.find('=') > -1:
            return raw_query[0: raw_query.find("=")].strip()
        else:
            return raw_query[0: raw_query.find("&")].strip()

    def get_filter(raw_query):
        if raw_query.find(' it') > -1:
            return QueryOperations.get_from_command("it")
        else:
            cmd = raw_query[raw_query.find("&"): raw_query.find(" ", raw_query.find("&"))]
            return QueryOperations.get_from_command(cmd)

    def get_data(raw_query):
        return raw_query[raw_query.find('"') + 1: raw_query.find('"', raw_query.find('"') + 1)] if raw_query.find(
            '"') > 0 else None

    def parse_filters(raw_query):
        field = get_field_name(raw_query)
        filter = get_filter(raw_query)
        query_obj.needed_query_methods.append({
            "field": field,
            "filter": filter,
            "data": get_data(raw_query)
        })

    for instruction in query.strip().split(","):
        query_instructions.append(instruction.strip())

    for raw_query in query_instructions:
        if raw_query.find("=") > -1:
            query_obj.required_field.append(get_field_name(raw_query))

        parse_filters(raw_query)

    return query_obj


if __name__ == "__main__":
    query = """ 
            name = it, 
            age = it, 
            city &eq "city_name" 
            """
    obj = hyperql_parser(query)

    for instruction in obj.needed_query_methods:
        print(instruction)
