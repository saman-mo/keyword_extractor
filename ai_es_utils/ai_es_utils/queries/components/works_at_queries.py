from typing import List, Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class WorksAtQuery(QueryComponent):
    def __init__(self,
                 works_at_field: str = "worksAt",
                 name: str = "works_at",
                 bool_type: str = "filter",
                 **kwargs):
        """
        The component produces a query that finds candidates working at the provided companies.
        Profiles are matched if the candidate is currently working at any of the
        requested companies.
        The kwargs are passed directly to the inner query_sting query.

        :param works_at_field: field name in payload.query holding list of strings
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """
        self.kwargs = kwargs
        self.fields = ["company^1.0"]
        self.payload_key = works_at_field
        self.bool_type = bool_type
        self.name = name

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        companies = payload.query.get(self.payload_key)
        if isinstance(companies, list):
            if len(companies) > 0:
                query = wrap_bool_query(self._build(companies), bool_type=self.bool_type)
                return QueryComponentResponse(query=query)
            else:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _build(self, companies: List[str]) -> Dict[str, Any]:
        _company_query = query_dict(
            "query_string",
            query=self._build_company_query_string(companies),
            fields=self.fields,
            type="best_fields",
            default_operator="or",
            **self.kwargs
        )
        return query_dict(
            "bool",
            should=[
                _company_query
            ],
            _name=self.name,
            minimum_should_match=1
        )

    def _build_company_query_string(self, companies: List[str]) -> str:
        tokenized_companies = [self._tokenize_company(c) for c in companies]
        tokenized_companies = [c for c in tokenized_companies if c]  # Clean empty strings
        if len(tokenized_companies) > 1:
            return " OR ".join(tokenized_companies)
        elif len(tokenized_companies) == 1:
            return tokenized_companies[0]
        else:
            return ""

    def _tokenize_company(self, company: str) -> str:
        tokens = [t.strip() for t in company.split(" ") if t.strip()]
        if len(tokens) > 1:
            return self._wrap_brackets(" AND ".join(tokens))
        elif len(tokens) == 1:
            return tokens[0]
        else:
            return ""

    @staticmethod
    def _wrap_brackets(string: str) -> str:
        return "(" + string + ")"


class WorksNotAtQuery(WorksAtQuery):
    def __init__(self,
                 works_not_at_field: str = "worksAtExclude",
                 name: str = "works_not_at",
                 **kwargs):
        """
        The component produces a query that finds candidates not working at the provided companies.
        Profiles are matched if the candidate is currently not working at any of the
        requested companies.
        The kwargs are passed directly to the inner query_sting query.

        :param works_not_at_field: field name in payload.query holding list of strings
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """

        super().__init__(
            name=name,
            **kwargs
        )
        self.payload_key = works_not_at_field

    def _build_company_query_string(self, companies: List[str]) -> str:
        return f"NOT ({super()._build_company_query_string(companies)})"


class WorksAtPreviouslyQuery(WorksAtQuery):
    def __init__(self,
                 works_at_previously_field: str = "previouslyAt",
                 name: str = "works_at_previously",
                 **kwargs):
        """
        The component produces a query that finds candidates that have been working at the provided companies.
        Profiles are matched if the candidate is previously working at any of the requested companies.
        The kwargs are passed directly to the inner query_sting query.

        :param works_at_previously_field: field name in payload.query holding list of strings
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """

        super().__init__(
            name=name,
            **kwargs
        )
        self.fields = ["previousCompanies^1.0"]
        self.payload_key = works_at_previously_field


class WorksNotAtPreviouslyQuery(WorksNotAtQuery):
    def __init__(self,
                 works_not_at_previously_field: str = "previouslyAtExclude",
                 name: str = "works_not_at_previously",
                 **kwargs):
        """
        The component produces a query that finds candidates that have not been working at the provided companies.
        Profiles are matched if the candidate has not been previously working at any of the requested companies.
        The kwargs are passed directly to the inner query_sting query.

        :param works_not_at_previously_field: field name in payload.query holding list of strings
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """

        super().__init__(name=name, **kwargs)
        self.fields = ["previousCompanies^1.0"]
        self.payload_key = works_not_at_previously_field
