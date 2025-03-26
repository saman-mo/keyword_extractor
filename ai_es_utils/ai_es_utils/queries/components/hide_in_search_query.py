from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class HideInSearchQuery(QueryComponent):
    def __init__(self, bool_type: str = "must_not", **kwargs):
        """
        The component produces a query that skips profiles flagged as `_hideInSearch=True`.
        The kwargs are passed directly to the inner match query.

        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match query
        """
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        query = wrap_bool_query(self._build(), bool_type=self.bool_type)
        return QueryComponentResponse(query=query)

    def _build(self):
        return query_dict("match", _hideInSearch=True, **self.kwargs)
