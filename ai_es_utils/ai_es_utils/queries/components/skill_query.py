from typing import List, Dict, Any

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import parse_boosted_fields, wrap_nested_field_query, apply_boost_factor, wrap_bool_query, \
    query_dict


class SkillQuery(QueryComponent):
    def __init__(self,
                 boosted_fields: List[str] = ("skills^3.0", "jobTitle^2.0", "previousJobTitles", "industry", "study"),
                 minimum_should_match=1,
                 name: str = "skill",
                 nested_bool: bool = False,
                 skills_field: str = "skills",
                 bool_type: str = "must",
                 boost_factor: float = None,
                 **kwargs):
        """
        The component produces a query based on the a list of skills. Each skill is matched
        in all fields provided in `target_fields`. On default each skill needs to be matched
        to at least one field (`minimum_should_match=1`).

        :param boosted_fields: list of elasticsearch fields in which to search for the skill string
        :param minimum_should_match: how much fields need to match the skill
        :param nested_bool: controls if fields should be considered nested or flat (e.g. "jobs.jobTitle")
        :param skills_field: field name in payload.query holding list of strings
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of kwargs directly passed to the most inner match_phrase query
        """
        self.boost_factor = boost_factor
        if self.boost_factor:
            boosted_fields = apply_boost_factor(boosted_fields, self.boost_factor)
        self.fields, self.boosts = parse_boosted_fields(boosted_fields)

        self.name = name
        self.minimum_should_match = minimum_should_match
        self.nested_bool = nested_bool
        self.skills_field = skills_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        skills = payload.query.get(self.skills_field)
        if skills:
            query = wrap_bool_query(self._build(skills), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, skills: List[str]) -> List[Dict[str, Any]]:
        must_queries = []
        for skill in skills:
            must_queries.append(
                query_dict(
                    "bool",
                    should=[
                        self._build_subquery(skill, field, boost) for field, boost in zip(self.fields, self.boosts)
                    ],
                    minimum_should_match=1
                )
            )
        return must_queries

    def _build_subquery(self, skill, field, boost) -> Dict[str, Any]:
        boost_dict = self._set_boost_query(boost)
        _query = query_dict(
            "match_phrase",
            **{field: {
                "query": skill,
                **self.kwargs,
                **boost_dict,
                "_name": f"{self.name}.{field}.{skill}"
            }}
        )
        if self.nested_bool:
            _query = wrap_nested_field_query(field, _query)
        return _query

    @staticmethod
    def _set_boost_query(boost):
        boost_dict = {}
        if boost:
            boost_dict["boost"] = boost
        return boost_dict
