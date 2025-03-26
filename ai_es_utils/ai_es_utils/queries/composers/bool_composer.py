from ai_es_utils.queries.interfaces.query_composer import QueryComposer, List
from ai_es_utils.queries.utils import update_nested_dict


class BoolQueryComposer(QueryComposer):
    def __init__(
            self,
            bool_fields: List[str] = ("must", "filter", "should", "must_not"),
            minimum_should_match: int = None,
            **kwargs
    ):
        """
        Composer that combines the produced sub-queries such that a list of inner `bool.should` queries are
        combined to a single `bool.should` sub-query.

        :param bool_fields: list of keys for the outer bool query that should be contracted.
        :param minimum_should_match: controls how many of the contracted `bool.should` queries are required to produce a hit
        """
        super().__init__(**kwargs)
        self._bool_fields = list(bool_fields)
        self._minimum_should_match = minimum_should_match

    def __call__(self, query_stack: List[dict], **kwargs) -> dict:
        self.reset()
        for sub_query in query_stack:
            self._query = update_nested_dict(sub_query, self._query)

        self._contract_nested_bool_queries()
        self._query.update(kwargs)
        self._query.update(self.kwargs)
        return self._query

    def _contract_nested_bool_queries(self):
        for field in self._bool_fields:
            try:
                self._query["query"]["bool"][field] = self._contract_sub_queries(
                    self._query["query"]["bool"][field]
                )
                if self._minimum_should_match:
                    self._query["query"]["bool"][field] = self._inject_minimum_should_match(
                        self._query["query"]["bool"][field]
                    )
            except KeyError:
                pass

    @staticmethod
    def _contract_sub_queries(sub_queries: List[dict]) -> List[dict]:
        _bool_should_query = dict()
        _other_queries = []
        for q in sub_queries:
            try:
                if isinstance(q["bool"]["should"], list):
                    _bool_should_query = update_nested_dict(q, _bool_should_query)
            except KeyError:
                _other_queries.append(q)

        if _bool_should_query:
            _other_queries.append(_bool_should_query)
        return _other_queries

    def _inject_minimum_should_match(self, sub_queries: List[dict]) -> List[dict]:
        _query_list = []
        for q in sub_queries:
            try:
                if "should" in q["bool"]:
                    q["bool"]["minimum_should_match"] = self._minimum_should_match
            except KeyError:
                pass
            finally:
                _query_list.append(q)
        return _query_list
