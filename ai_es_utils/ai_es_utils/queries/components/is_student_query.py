from ai_es_utils.queries.components.boolean_filter_query_component import BooleanFilterQueryComponent


class IsStudentQuery(BooleanFilterQueryComponent):
    def __init__(self, students_only_field: str = "studentsOnly", **kwargs):
        """
        The component produces a query that filters candidates that are currently students.
        The kwargs are passed directly to the inner term query.

        :param students_only_field: field name in payload.query holding bool
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        super().__init__(**kwargs)
        self.payload_key = students_only_field
        self.term_query_key = "isStudent"
