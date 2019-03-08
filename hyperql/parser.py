""" Parser module help to parse hyperQl query language to an plan python object """


class QueryOperations:
    """
    Hold the all operations for querying data.
    all methods of this class is called during iteration and
    "data" :argument is immutable and treated as constant but
    "field" :argument is mutable that changed in every iteration
    """

    @staticmethod
    def equal_to(data, field):
        """
        just for equal ("=") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after equal check
        """
        return data == field

    @staticmethod
    def not_equal_to(data, field):
        """
        just for not equal ("!=") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after not equal check
        """
        return data != field

    @staticmethod
    def greater_than(data, field):
        """
        just for not equal (">") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after greater than check
        """
        return data > field

    @staticmethod
    def less_than(data, field):
        """
        just for not equal ("<") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after less than check
        """
        return data < field

    @staticmethod
    def greater_than_equal(data, field):
        """
        just for not equal (">=") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after greater than equal check
        """
        return data >= field

    @staticmethod
    def less_than_equal(data, field):
        """
        just for not equal ("<=") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after less than equal check
        """
        return data <= field

    @staticmethod
    def and_operation(data, field):
        """
        just for not equal ("&") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after and operation
        """
        return data and field

    @staticmethod
    def or_operation(data, field):
        """
        just for not equal ("|") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after or operation
        """
        return data or field

    @staticmethod
    def not_operation(field):
        """
        just for not equal ("!") operation
        :param data: its a immutable data that passed by user via hyperQl
        :param field: its a mutable and point to actual field data in collection
        :return: Boolean after not operation
        """
        return not field

    @staticmethod
    def get_from_command(cmd):
        """
        :param cmd: is a special code or key to determine the actual operation
        :return: method reference as a operation of QueryOperation :class
        """
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
    """ Schema of actual hyperQl in plan python object """

    def __init__(self):
        self.view = []
        self.selective = []
        self.modifiers = {
            "limit": -1,
            "skip": 0
        }


def parser(query: str) -> Query:
    """
    Main method that's parse the raw hyperQL into hyperlite database engine understandable form
    :param query: takes hyperQl query as a string
    :return: object of Query :query_obj
    """

    query_obj = Query()

    def get_field_name(raw_query):
        """
        :param raw_query: single instruction of whole query that passed to main :parser method
        :return: the field name from raw instruction
        """
        if raw_query.find('&') > -1:
            return raw_query[0: raw_query.find("&")].strip()
        else:
            return raw_query if raw_query.find(' ') == -1 else None

    def get_filter(raw_query):
        """
        :param raw_query: single instruction of whole query that passed to main :parser method
        :return: method reference as a operation of QueryOperation :class
        """
        if raw_query.find('&') > -1:
            cmd = raw_query[raw_query.find("&"): raw_query.find(" ", raw_query.find("&"))]
            return QueryOperations.get_from_command(cmd)
        else:
            return None

    def get_data(raw_query):
        """
        :param raw_query: single instruction of whole query that passed to main :parser method
        :return: data that passed by user via hyperQl selective Query
        """
        raw_data = (raw_query[raw_query.find(' ', raw_query.find(' ') + 1) + 1: len(raw_query)])
        if raw_data.find('"') > -1:
            return raw_query[raw_query.find('"') + 1: raw_query.find('"', raw_query.find('"') + 1)] if raw_query.find(
                '"') > 0 else None
        else:
            if raw_data.lower() == 'true':
                return True
            elif raw_data.lower() == 'false':
                return False
            return int(raw_data)

    def parse_filters(raw_query):
        """
        Method that actual parse the filters from rawHyperQl
        :param raw_query: single instruction of whole query that passed to main :parser method
        :return: :None
        """
        field = get_field_name(raw_query)
        filter = get_filter(raw_query)
        query_obj.selective.append({
            "field": field,
            "filter": filter,
            "data": get_data(raw_query)
        })

    def parse_modifiers(raw_query):
        """
        Method that actual parse the Modifiers from rawHyperQl
        :param raw_query: single instruction of whole query that passed to main :parser method
        :return: :None
        """
        if 'limit' in raw_query:
            query_obj.modifiers['limit'] = int(raw_query[raw_query.find(':') + 1: len(raw_query)].strip())
        if 'skip' in raw_query:
            query_obj.modifiers['skip'] = int(raw_query[raw_query.find(':') + 1: len(raw_query)].strip())
        if 'sort' in raw_query:
            query_obj.modifiers['sort'] = raw_query[raw_query.find(':') + 1: len(raw_query)].strip()

    # Main Entry point of parser method with just O(N) Time Complexity
    instructions = query.strip().split(",")
    if instructions[len(instructions) - 1] == '':
        instructions.pop()
    for raw_query in instructions:
        raw_query = raw_query.strip()
        if raw_query.find(' ') == -1:
            field_name = get_field_name(raw_query)
            if field_name == '*':
                query_obj.view = field_name
            else:
                query_obj.view.append(field_name) if type(query_obj.view) is list else '*'
        if raw_query.find('$') > -1:
            parse_modifiers(raw_query)
        elif raw_query.find('&') > -1:
            parse_filters(raw_query)

    return query_obj


if __name__ == "__main__":
    query = """ 
            *,name,
            email &eq "username@domain.com", 
            city &eq "city_name",
            age &gt 18,
            isBlocked &eq False,
            $skip : 5,
            $limit : 104,
            $sort : -name
            """
    obj = parser(query)
    print(obj.view)
    for instruction in obj.selective:
        print(instruction)

    print(obj.modifiers)
