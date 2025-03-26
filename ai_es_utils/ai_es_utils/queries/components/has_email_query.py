from ai_es_utils.queries.components.boolean_filter_query_component import BooleanFilterQueryComponent


class HasEmailQuery(BooleanFilterQueryComponent):
    def __init__(self, has_email_field: str = "hasEmail", **kwargs):
        """
        The component produces a query that filters for candidates that have an e-mail.
        The kwargs are passed directly to the inner term query.

        :param has_email_field: field name in payload.query holding bool
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        super().__init__(**kwargs)
        self.payload_key = has_email_field
        self.term_query_key = "hasEmail"
