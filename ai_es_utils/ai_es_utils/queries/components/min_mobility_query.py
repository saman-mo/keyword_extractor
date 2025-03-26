from typing import Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class MinMobilityQuery(QueryComponent):
    def __init__(self,
                 mobility_field: str = "mobility",
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query filters candidates that meet the requirements
        to a minimum value for the mobility.
        The kwargs are passed directly to the inner range query.

        :param mobility_field: field name in payload.query holding int
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal range query
        """
        self.mobility_field = mobility_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        min_mobility = payload.query.get(self.mobility_field)
        if isinstance(min_mobility, int):
            query = wrap_bool_query(self._build(min_mobility), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, min_mobility: int) -> Dict[str, Any]:
        return query_dict("range", mobility={"gte": min_mobility}, **self.kwargs)
