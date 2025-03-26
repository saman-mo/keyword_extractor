from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class IndustryCodeQuery(QueryComponent):
    def __init__(self,
                 industry_code_field: str = "industryCode",
                 nested_bool: bool = False,
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query searches for a specified industry code in the jobs entries.
        The kwargs are passed directly to the inner term query.

        :param industry_code_field: field name in payload.query holding string
        :param nested_bool: False on default. If true, builds query for nested fields if provided
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.industry_code_field = industry_code_field
        self.nested_bool = nested_bool
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        industry_code = payload.query.get(self.industry_code_field)
        if isinstance(industry_code, str):
            query = wrap_bool_query(self._build(industry_code), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, industry_code: str) -> dict:
        _query = query_dict("term", **{
            "jobs.industryCode": industry_code,
            **self.kwargs
        })

        if self.nested_bool:
            _query = query_dict(
                "nested",
                path="jobs",
                query=_query
            )

        return _query
