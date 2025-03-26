from ai_es_utils.queries.components.boolean_filter_query_component import BooleanFilterQueryComponent


class IsEntrepreneurQuery(BooleanFilterQueryComponent):
    def __init__(self, entrepreneur_only_field: str = "entrepreneursOnly", **kwargs):
        """
        The component produces a query that filters for candidates that are entrepreneurs.
        The kwargs are passed directly to the inner term query.

        :param entrepreneur_only_field: field name in payload.query holding bool
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        super().__init__(**kwargs)
        self.payload_key = entrepreneur_only_field
        self.term_query_key = "isEntrepreneur"
