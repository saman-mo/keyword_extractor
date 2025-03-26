from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class ExcludePortalsQuery(QueryComponent):
    def __init__(self,
                 exclude_portals_field: str = "excludePortals",
                 bool_type: str = "must_not",
                 **kwargs):
        """
        The component produces a query that filters out certain networks that are
        listed in the "excludePortals" key. Takes kwargs that are handed down to
        the inner "terms" query.

        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param exclude_portals_field: field name in payload.query listing networks to exclude
        :param kwargs: dictionary of arguments passed directly to the internal terms query
        """
        self.exclude_portals_field = exclude_portals_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        exclude_portals = payload.query.get(self.exclude_portals_field)
        if isinstance(exclude_portals, list):
            if len(exclude_portals) > 0:
                query = wrap_bool_query(self._build(exclude_portals), bool_type=self.bool_type)
                return QueryComponentResponse(query=query)
            else:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _build(self, exclude_portals: List[str]) -> dict:
        return query_dict(
            "terms",
            _class=exclude_portals,
            **self.kwargs
        )
