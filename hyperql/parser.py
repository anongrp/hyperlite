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
    def get_from_command(cmd):
        operations = {
            "&eq": QueryOperations.equal_to,
            "&neq": QueryOperations.not_equal_to,
            "&gt": QueryOperations.greater_than,
            "&lt": QueryOperations.less_than,
            "&gte": QueryOperations.greater_than_equal,
            "&lte": QueryOperations.less_than_equal
        }
        return operations.get(cmd)


class Query:
    def __init__(self):
        self.required_field = []
        self.needed_query_methods = []
        self.modifiers = {
            "limit": -1,
            "skip": 0
        }


def hyperql_parser(query: str) -> Query:
    query_obj = Query()
    query_instructions = []

    def get_field_name(raw_query):
        if raw_query.find('&') > -1:
            return raw_query[0: raw_query.find("&")].strip()
        else:
            return raw_query if raw_query.find(' ') == -1 else None

    def get_filter(raw_query):
        if raw_query.find('&') > -1:
            cmd = raw_query[raw_query.find("&"): raw_query.find(" ", raw_query.find("&"))]
            return QueryOperations.get_from_command(cmd)
        else:
            return None

    def get_data(raw_query):
        raw_data = (raw_query[raw_query.find(' ', raw_query.find(' ') + 1) + 1: len(raw_query)])
        if raw_data.find('"') > -1:
            return raw_query[raw_query.find('"') + 1: raw_query.find('"', raw_query.find('"') + 1)] if raw_query.find(
                '"') > 0 else None
        else:
            return int(raw_data)

    def parse_filters(raw_query):
        field = get_field_name(raw_query)
        filter = get_filter(raw_query)
        query_obj.needed_query_methods.append({
            "field": field,
            "filter": filter,
            "data": get_data(raw_query)
        })

    def parse_modifiers(raw_query):
        if 'limit' in raw_query:
            query_obj.modifiers['limit'] = int(raw_query[raw_query.find(':') + 1: len(raw_query)].strip())
        if 'skip' in raw_query:
            query_obj.modifiers['skip'] = int(raw_query[raw_query.find(':') + 1: len(raw_query)].strip())
        if 'sort' in raw_query:
            query_obj.modifiers['sort'] = raw_query[raw_query.find(':') + 1: len(raw_query)].strip()

    for instruction in query.strip().split(","):
        query_instructions.append(instruction.strip())

    for raw_query in query_instructions:
        if raw_query.find(' ') == -1:
            field_name = get_field_name(raw_query)
            if field_name == '*':
                query_obj.required_field = field_name
            else:
                query_obj.required_field.append(field_name) if type(query_obj.required_field) is list else '*'
        if raw_query.find('$') > -1:
            parse_modifiers(raw_query)
        elif raw_query.find('&') > -1:
            parse_filters(raw_query)

    return query_obj


if __name__ == "__main__":
    query = """ 
            *,
            email &eq "username@domain.com", 
            city &eq "city_name",
            age &gt 18,
            $skip : 5,
            $limit : 104,
            $sort : -name
            """
    obj = hyperql_parser(query)

    print(obj.required_field)
    for instruction in obj.needed_query_methods:
        print(instruction)

    print(obj.modifiers)
