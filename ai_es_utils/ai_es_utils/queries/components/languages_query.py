from typing import List, Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class LanguagesQuery(QueryComponent):
    def __init__(self,
                 language_field: str = "languages",
                 boost: float = 1.0,
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query that finds candidates speaking all languages in the requested list.
        The kwargs are passed directly to the inner query_string query.

        :param language_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """
        self.kwargs = kwargs
        self.language_field = language_field
        self.bool_type = bool_type
        self.boost = boost

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        languages = payload.query.get(self.language_field)
        if isinstance(languages, list):
            if len(languages) > 0:
                query = wrap_bool_query(self._build(languages), bool_type=self.bool_type)
                return QueryComponentResponse(query=query)
            else:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _build(self, languages: List[str]) -> Dict[str, Any]:
        return query_dict(
            "query_string",
            query=" AND ".join(languages),
            fields=[f"languagesString^{self.boost}"],
            default_operator="and",
            type="best_fields",
            **self.kwargs
        )
