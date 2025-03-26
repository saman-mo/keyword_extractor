from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class IncludePortalsQuery(QueryComponent):
    def __init__(self,
                 include_portals_field: str = "includePortals",
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query that filters out profiles **not** from the specified
        networks that are listed in the "includePortals" key. Takes kwargs that are handed
        down to the inner "terms" query.

        :param include_portals_field: field name in payload.query holding list of strings
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal terms query
        """
        self.include_portals_field = include_portals_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        include_portals = payload.query.get(self.include_portals_field)
        if isinstance(include_portals, list):
            if len(include_portals) > 0:
                query = wrap_bool_query(self._build(include_portals), bool_type=self.bool_type)
                return QueryComponentResponse(query=query)
            else:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _build(self, include_portals: List[str]) -> dict:
        return query_dict(
            "terms",
            _class=include_portals,
            **self.kwargs
        )
