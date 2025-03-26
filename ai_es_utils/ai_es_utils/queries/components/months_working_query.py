from typing import Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class MonthsWorkingQuery(QueryComponent):
    def __init__(self,
                 years_working_min_field: str = "yearsWorkingMin",
                 years_working_max_field: str = "yearsWorkingMax",
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query that filters candidates by the number of months they are working.
        The kwargs are passed directly to the inner range query.

        :param years_working_min_field: field name in payload.query holding int
        :param years_working_max_field: field name in payload.query holding int
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.years_working_min_field = years_working_min_field
        self.years_working_max_field = years_working_max_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        years_working_min = payload.query.get(self.years_working_min_field)
        years_working_max = payload.query.get(self.years_working_max_field)

        if isinstance(years_working_min, int) or isinstance(years_working_max, int):
            query = wrap_bool_query(self._build(years_working_min, years_working_max), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, years_working_min: int, years_working_max: int) -> Dict[str, Any]:
        return query_dict(
            "range",
            monthsWorking=self._build_bounds(years_working_min, years_working_max),
            **self.kwargs
        )

    @staticmethod
    def _build_bounds(years_working_min: int, years_working_max: int):
        bounds = {
            "include_lower": years_working_min is not None,
            "include_upper": years_working_max is not None
        }

        if years_working_min:  # TODO: We could validate that we get reasonable values here, e.g. no negatives and smaller then 100. Could be also validated in basemodel.
            bounds["from"] = years_working_min * 12
        if years_working_max:
            bounds["to"] = years_working_max * 12

        return bounds
