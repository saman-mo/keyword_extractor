from typing import Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class MinChangeProbabilityQuery(QueryComponent):
    def __init__(self,
                 change_probability_field: str = "changeProbability",
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query filters candidates that meet the requirements
        to a minimum value for the change probability.
        The kwargs are passed directly to the inner range query.

        :param change_probability_field: field name in payload.query holding int
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal range query
        """
        self.change_probability_field = change_probability_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        min_change_probability = payload.query.get(self.change_probability_field)
        if isinstance(min_change_probability, int):
            query = wrap_bool_query(self._build(min_change_probability), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, min_change_probability: int) -> Dict[str, Any]:
        return query_dict("range", changeProbability={"gte": min_change_probability}, **self.kwargs)
