from ai_es_utils.queries.components.boolean_filter_query_component import BooleanFilterQueryComponent


class IsRecruiterQuery(BooleanFilterQueryComponent):
    def __init__(self, recruiter_only_field: str = "recruiterOnly", **kwargs):
        """
        The component produces a query that filters candidates are working as a recruiter.
        The kwargs are passed directly to the inner term query.

        :param recruiter_only_field: field name in payload.query holding bool
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        super().__init__(**kwargs)
        self.payload_key = recruiter_only_field
        self.term_query_key = "isRecruiter"
