from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class GenderQuery(QueryComponent):
    def __init__(self,
                 is_male_field: str = "isMale",
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query that filters for male or female candidates.
        The kwargs are passed directly to the inner term query.

        :param is_male_field: field name in payload.query holding bool
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.is_male_field = is_male_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        is_male = payload.query.get(self.is_male_field)
        if isinstance(is_male, bool):
            query = wrap_bool_query(self._build(is_male), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, is_male: bool) -> dict:
        _gender_str = "f"
        if is_male:
            _gender_str = "m"

        return query_dict("term", gender=_gender_str, **self.kwargs)
