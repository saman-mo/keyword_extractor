from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class BooleanFilterQueryComponent(QueryComponent):
    def __init__(self, bool_type: str = "filter", **kwargs):
        """
        Base template for repeating is-filter queries. Queries filter candidates
        according to the boolean value of the `term_query_key`. The expected
        boolean value is set from the payload (`payload_key`).

        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.kwargs = kwargs
        self.bool_type = bool_type
        self.payload_key = None
        self.term_query_key = None

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        value = payload.query.get(self.payload_key)
        if isinstance(value, bool):
            query = wrap_bool_query(self._build(value), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, value: bool) -> dict:
        return query_dict(
            "term",
            **{
                self.term_query_key: value,
                **self.kwargs
            }
        )
