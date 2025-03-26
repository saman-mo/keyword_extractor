from typing import Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class LocationQuery(QueryComponent):
    def __init__(self,
                 location_field: str = "location",
                 bool_type: str = "should",
                 **kwargs):
        """
        The component produces a query that searches for an optional match of the provided
        location, i.e. by name instead of geo-point distance.
        The kwargs are passed directly to the inner match query.

        :param location_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match query
        """
        self.location_field = location_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        location = payload.query.get(self.location_field)
        if isinstance(location, str):
            query = wrap_bool_query(self._build(location), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, location: str) -> Dict[str, Any]:
        return query_dict("match", location=location, **self.kwargs)
