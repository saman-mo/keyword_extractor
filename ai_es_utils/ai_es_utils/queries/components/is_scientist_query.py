from ai_es_utils.queries.components.boolean_filter_query_component import BooleanFilterQueryComponent


class IsScientistQuery(BooleanFilterQueryComponent):
    def __init__(self, scientist_only_field: str = "scientistsOnly", **kwargs):
        """
        The component produces a query that filters for candidates
        that work as scientists or in research.
        The kwargs are passed directly to the inner term query.

        :param scientist_only_field: field name in payload.query holding bool
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        super().__init__(**kwargs)
        self.payload_key = scientist_only_field
        self.term_query_key = "isScientist"
