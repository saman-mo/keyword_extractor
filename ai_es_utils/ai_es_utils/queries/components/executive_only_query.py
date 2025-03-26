from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, build_field_path_map, parse_boosted_fields, query_dict


class ExecutiveOnlyQuery(QueryComponent):
    def __init__(self, curated_executive_sub_query: str = None,
                 fields: List[str] = None,
                 name: str = "executive_only",
                 executive_only_field: str = "executiveOnly",
                 nested_bool: bool = False,
                 bool_type_include: str = "filter",
                 bool_type_exclude: str = "must_not",
                 **kwargs):
        """
        The component builds a query that filters job titles that are belonging to
        candidates in an executive position. In particular, job titles are checked
        against a curated query, such as 'Chief OR Vertriebsleit* OR ai_es_utils.queries..'. If
        `executiveOnly=True`, candidates are required to match the above
        query, else candidates matching the above query are ignored.

        TODO: Both sub-queries are necessary as sometimes a job is listed under jobs.jobTitle but not in jobTitle or previousJobTitle, as well as the other way around. Its seems hard to find a better way to query nested and top-level keys at the same time.

        :param curated_executive_sub_query: String containing a curated query filtering
               job titles belonging to candidates in executive positions,
               e.g. 'Chief OR Vertriebsleit* OR ai_es_utils.queries..'
        :param fields: List of fields the query is applied to.
        :param name: name of the named query
        :param executive_only_field: field name in payload.query holding bool
        :param nested_bool: False on default. If true, builds query for nested fields if provided
        :param bool_type_include: type of outer boolean query (filter, must, must_not, should)
        :param bool_type_exclude: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """
        self.curated_executive_sub_query = curated_executive_sub_query
        self.kwargs = kwargs
        self.name = name
        self.executive_only_field = executive_only_field
        self.nested_bool = nested_bool
        self.bool_type_include = bool_type_include
        self.bool_type_exclude = bool_type_exclude

        self.fields = fields
        if self.fields:
            self.fields, _ = parse_boosted_fields(fields)
        if not self.fields:
            self.fields = ["jobTitle", "previousJobTitles", "jobs.jobTitle"]

        self.nested_field_map = dict()
        if self.nested_bool:
            self.nested_field_map = build_field_path_map(self.fields, [0.0] * len(self.fields))

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        executive_only = payload.query.get(self.executive_only_field)

        if isinstance(executive_only, bool):
            return QueryComponentResponse(query=self._build(executive_only))
        else:
            return QueryComponentResponse(query={})

    def _build(self, executive_only_bool: bool) -> dict:
        if self.nested_bool:
            sub_query = self._build_nested_sub_query()
        else:
            sub_query = self._build_query_string_query(self.fields, name=self.name)

        if executive_only_bool:
            return wrap_bool_query(sub_query, bool_type=self.bool_type_include)
        else:
            return wrap_bool_query(sub_query, bool_type=self.bool_type_exclude)

    def _build_nested_sub_query(self) -> dict:
        should_queries = [self._build_nested_query(path, fields)
                          for path, fields in self.nested_field_map.items() if path != "None"]
        should_queries.append(self._build_query_string_query(self.nested_field_map["None"]))

        return query_dict(
            "bool",
            should=should_queries,
            _name=self.name,
            minimum_should_match=1
        )

    def _build_nested_query(self, path: str, fields: List[str]):
        return query_dict(
            "nested",
            path=path,
            query=self._build_query_string_query([f"{path}.{field}" for field in fields])
        )

    def _build_query_string_query(self, fields: List[str], name: str = None):
        name_dict = {}
        if name:
            name_dict = {"_name": name}

        return query_dict(
            "query_string",
            fields=fields,
            query=self.curated_executive_sub_query,
            type="best_fields",
            default_operator="or",
            **name_dict,
            **self.kwargs
        )
