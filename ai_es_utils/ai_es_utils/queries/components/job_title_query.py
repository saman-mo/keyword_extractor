import itertools
from typing import List, Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import parse_boosted_fields, generalize_gender_map, wrap_nested_field_query, \
    apply_boost_factor, wrap_bool_query, query_dict


class JobTitleQuery(QueryComponent):
    def __init__(self,
                 boosted_fields: List[str] = None,
                 gender_normalization_map: dict = None,
                 name: str = "job_title",
                 nested_bool: bool = False,
                 boost_factor: float = None,
                 job_title_field: str = "jobTitle",
                 bool_type: str = "must",
                 **kwargs):
        """
        The component produces a query based on the job title. If a gender normalization map was provided, the job title
        is extended to its gender variants and the query contains a list of "should-match" job titles, where one of
        which needs to match.

        :param boosted_fields: list of fields in boosted format, e.g. "field^2.0"
        :param gender_normalization_map: dictionary mapping from neutral job titles to all known gender variants
        :param minimum_should_match: number of job titles that need to match, default is 1
        :param name: name of the query group
        :param nested_bool: controls if fields should be considered nested or flat (e.g. "jobs.jobTitle")
        :param boost_factor: global boost factor multiplied to all boost values of all fields
        :param job_title_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match_phrase query
        """
        self.boosted_fields = boosted_fields
        if not self.boosted_fields:
            self.boosted_fields = ["jobTitle^2.0", "previousJobTitles"]

        if boost_factor:
            self.boosted_fields = apply_boost_factor(self.boosted_fields, boost_factor)

        self.fields, self.boosts = parse_boosted_fields(list(self.boosted_fields))
        self.gender_normalization_map = generalize_gender_map(gender_normalization_map)
        self.name = name
        self.nested_bool = nested_bool
        self.job_title_field = job_title_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        job_title = payload.query.get(self.job_title_field)
        if isinstance(job_title, str):
            query = wrap_bool_query(self._build(job_title.lower()), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, job_title: str) -> dict:
        return query_dict(
            "bool",
            should=self._get_job_query_variants(job_title),
            _name=self.name,
        )

    def _get_job_query_variants(self, job_title) -> List[Dict[str, Any]]:
        gender_variants = self._get_gender_variants(job_title)
        sub_query_groups = [
            self._build_sub_query(gender_variants, field, boost) for field, boost in zip(self.fields, self.boosts)
        ]
        return list(itertools.chain.from_iterable(sub_query_groups))

    def _get_gender_variants(self, job_title):
        return self.gender_normalization_map.get(job_title, self._build_default_gender_data(job_title))

    @staticmethod
    def _build_default_gender_data(job_title):
        return {
            "male": {"jobTitle": job_title},
            "normalized": {"jobTitle": job_title}
        }

    def _build_sub_query(self, gender_variants, field, boost):
        boost_dict = self._set_boost_dict(boost)

        normalized_job_title = gender_variants["normalized"]["jobTitle"]
        query_name = f"{self.name}.{field}.{normalized_job_title}"

        sub_query = []
        for gender, job_dict in gender_variants.items():
            if gender in ["male", "female"]:
                sub_query.append( self._build_specific_sub_query(field, job_dict["jobTitle"], boost_dict, query_name))
        return sub_query

    def _build_specific_sub_query(self, field, query, boost_dict, query_name):
        _query = query_dict("match_phrase", **{
            field: {
                "query": query,
                **boost_dict,
                "_name": query_name,
                **self.kwargs
            }
        })

        if self.nested_bool:
            return wrap_nested_field_query(
                field,
                _query
            )
        else:
            return _query

    @staticmethod
    def _set_boost_dict(boost):
        boost_dict = {}
        if boost:
            boost_dict["boost"] = boost
        return boost_dict
