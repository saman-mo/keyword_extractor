from ai_es_utils.queries.components.boolean_filter_query_component import BooleanFilterQueryComponent


class IsConsultantQuery(BooleanFilterQueryComponent):
    def __init__(self, consultant_only_field: str = "consultantsOnly", **kwargs):
        """
        The component produces a query that filters for candidates that work as a consultant.
        The kwargs are passed directly to the inner term query.

        :param consultant_only_field: field name in payload.query holding bool
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        super().__init__(**kwargs)
        self.payload_key = consultant_only_field
        self.term_query_key = "isConsultant"
