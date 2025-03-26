from typing import List, Dict, Any, Optional

from ai_es_utils.queries.components.job_title_query import JobTitleQuery
from ai_es_utils.queries.interfaces import QueryComponentResponse
from ai_es_utils.queries.models import SemanticExpansion, RequestPayload
from ai_es_utils.queries.utils import build_field_path_map, format_boosted_field, wrap_bool_query, query_dict
from ai_es_utils.services import RequestError
from ai_es_utils.services.enrichment import Job2SkillsService


def quote(word):
    w = word.strip('"')
    return f' "{w.replace("/", "//")}" '


class SkillExpansionQuery(JobTitleQuery):
    def __init__(
            self,
            job2skills_service: Job2SkillsService,
            boosted_fields: List[str] = ("skills^3.0", "jobTitle^2.0", "previousJobTitles"),
            gender_normalization_map: dict = None,
            curated_skills_expansion: dict = None,
            name: str = "job_title_expansion",
            nested_bool: bool = False,
            job_title_field: str = "jobTitle",
            bool_type: str = "must",
            boost_factor: float = None,
            **kwargs
    ):
        """
        The component produces a query searching for skills that are similar to the queried job title.
        If the job title is contained in a list of curated skills, the curated list is used. Else, the
        similar jobs are requested from the Job2SkillsService.
        The suggested skills are writen to the payload under "payload.query.semanticExpansion.skills",
        which tracks the user response (i.e. declining suggested skills). If the payload already
        contains a valid semanticExpansion, these suggestions are used instead.

        The kwargs are passed directly to the inner `query_string` query.

        :param job2skills_service: service serving similar skills to jobs
        :param gender_normalization_map: dictionary mapping from neutral job titles to all known gender variants
        :param minimum_should_match: minimum number of expanded skills that need to match
        :param curated_skills_expansion: dictionary holding curated list of skills to serve for certain job titles
        :param name: name of the query group
        :param job_title_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """
        super().__init__(
            boosted_fields=boosted_fields,
            gender_normalization_map=gender_normalization_map,
            name=name,
            nested_bool=nested_bool,
            job_title_field=job_title_field,
            bool_type=bool_type,
            boost_factor=boost_factor,
            **kwargs
        )
        self.job2skills_service = job2skills_service
        self.curated_skills_expansion = curated_skills_expansion

        self.field_path_map = None
        if self.nested_bool:
            self.field_path_map = build_field_path_map(self.fields, self.boosts)

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        job_title = payload.query.get(self.job_title_field)
        if isinstance(job_title, str):
            try:
                semantic_expansion_skills = self._get_semantic_expansion(payload, bearer_token=bearer_token)
                return QueryComponentResponse(
                    query=self._build(semantic_expansion_skills),
                    response_data={"semanticExpansion": {"skills": semantic_expansion_skills}}
                )
            except RequestError:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _get_semantic_expansion(self, payload, bearer_token: str = None) -> List[Dict[str, Any]]:
        job_title = payload.query.get(self.job_title_field).lower()
        _provided_semantic_expansion = self._set_provided_semantic_expansion(payload)

        if _provided_semantic_expansion.skills is None:
            skills_expansion = self._get_skill_expansion(job_title, bearer_token=bearer_token)
            semantic_expansion_skills = self._format_as_semantic_expansion(skills_expansion)
        else:
            semantic_expansion_skills = payload.query.get("semanticExpansion").skills

        return semantic_expansion_skills

    @staticmethod
    def _set_provided_semantic_expansion(payload: RequestPayload) -> SemanticExpansion:
        _provided_semantic_expansion = SemanticExpansion(jobs=None, skills=None)
        if payload.query.get("semanticExpansion") is not None:
            _provided_semantic_expansion = payload.query.get("semanticExpansion")
        return _provided_semantic_expansion

    def _get_skill_expansion(self, job_title: str, bearer_token: str = None) -> List[str]:
        skill_expansion = None
        if self.curated_skills_expansion:
            skill_expansion = self._fetch_curated_skill_expansion(job_title)
        if skill_expansion is None:
            skill_expansion = self.job2skills_service(job_title, bearer_token=bearer_token).keys()
        return skill_expansion

    def _fetch_curated_skill_expansion(self, job_title: str) -> List[str]:
        gender_variants = self.gender_normalization_map.get(job_title, [job_title])
        if isinstance(gender_variants, dict):
            gender_variants = [v["jobTitle"] for k, v in gender_variants.items()]
        for job in gender_variants:
            if job in self.curated_skills_expansion:
                return self.curated_skills_expansion[job]

    @staticmethod
    def _format_as_semantic_expansion(job_list: List[str]) -> List[Dict[str, Any]]:
        return [{"name": j, "isChecked": True} for j in job_list]

    def _build(self, semantic_expansion_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        query_string = [quote(s["name"]) for s in semantic_expansion_skills if s["isChecked"]]
        sub_queries = []
        if len(query_string) >= 1:
            sub_queries = self._build_sub_queries(" OR ".join(query_string))

        if sub_queries:
            return wrap_bool_query(self._build_valid(sub_queries), bool_type=self.bool_type)
        else:
            return {}

    def _build_valid(self, sub_queries) -> Dict[str, Any]:
        return query_dict(
            "bool",
            should=sub_queries,
            _name=self.name
        )

    def _build_sub_queries(self, query_string: str) -> List[Dict[str, Any]]:
        if self.nested_bool:
            return self._build_nested_sub_queries(query_string)
        else:
            return [self._build_query_string_query(
                query_string,
                [format_boosted_field(field, boost) for field, boost in zip(self.fields, self.boosts)],
                _name=f"{self.name}.skill_expansion"
            )]

    def _build_nested_sub_queries(self, query_string: str) -> List[Dict[str, Any]]:
        sub_queries = []
        for path, fields in self.field_path_map.items():
            if path == "None":
                sub_queries.append(
                    self._build_query_string_query(
                        query_string,
                        fields,
                        _name=f"{self.name}.skill_expansion"
                    )
                )
            else:
                sub_queries.append(
                    query_dict(
                        "nested",
                        path=path,
                        query=self._build_query_string_query(
                            query_string,
                            [path + "." + field for field in fields]
                        ),
                        _name=f"{self.name}.{path}.skill_expansion"
                    )
                )
        return sub_queries

    def _build_query_string_query(self, query_string: str, fields: List[str], **kwargs) -> Dict[str, Any]:
        return query_dict(
            "query_string",
            query=query_string,
            fields=fields,
            type="cross_fields",
            default_operator="AND",
            **kwargs,
            **self.kwargs
        )
