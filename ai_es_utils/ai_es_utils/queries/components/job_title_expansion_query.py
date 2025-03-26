from typing import List, Dict, Any

from ai_es_utils.queries.components.job_title_query import JobTitleQuery
from ai_es_utils.queries.interfaces import QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload, SemanticExpansion
from ai_es_utils.queries.utils import wrap_bool_query, query_dict
from ai_es_utils.services import RequestError
from ai_es_utils.services.enrichment import Job2JobsService


class JobTitleExpansionQuery(JobTitleQuery):
    def __init__(
            self,
            job2jobs_service: Job2JobsService,
            boosted_fields: List[str] = None,
            gender_normalization_map: dict = None,
            curated_jobs_expansion: dict = None,
            name: str = "job_title_expansion",
            nested_bool: bool = False,
            job_title_field: str = "jobTitle",
            bool_type: str = "must",
            boost_factor: float = None,
            **kwargs
    ):
        """
        The component produces a query searching for jobs that are similar to the queried job title.
        If the job title is contained in a list of curated similar job titles, the curated list is
        used. Else, the similar jobs are requested from the Job2JobsService.
        The suggested jobs are writen to the payload under "payload.query.semanticExpansion.jobs",
        which tracks the user response (i.e. declining suggested job titles). If the payload already
        contains a valid semanticExpansion, these suggestions are used instead.

        In all cases, all jobs are expanded to all gender variants known, as provided by the
        `gender_normalization_map`.

        The kwargs are passed directly to the inner `match_phrase` query.

        :param boosted_fields: list of fields in boosted format, e.g. "field^2.0"
        :param job2jobs_service: service serving similar jobs to the query job
        :param gender_normalization_map: dictionary mapping from neutral job titles to all known gender variants
        :param minimum_should_match: minimum number of general should match query
        :param curated_jobs_expansion: dictionary holding curated list of jobs to serve for certain job titles
        :param name: name of the query group
        :param nested_bool: controls if fields should be considered nested or flat (e.g. "jobs.jobTitle")
        :param job_title_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match_phrase query
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

        self.job2jobs_service = job2jobs_service
        self.curated_jobs_expansion = self._generalize_curated_jobs_expansion(curated_jobs_expansion)

    def _generalize_curated_jobs_expansion(self, curated_jobs_expansion):
        if curated_jobs_expansion:
            return {k: {"neutral": v, "specific": self._gender_expand_list(v)} for k, v in
                    curated_jobs_expansion.items()}
        else:
            return None

    def _gender_expand_list(self, job_list):
        if self.gender_normalization_map:
            _gender_variants = [
                self._get_gender_variants(job) for job in job_list
            ]
            _specific_gender_variants = []
            for data in _gender_variants:
                _specific_gender_variants.extend([v["jobTitle"] for k, v in data.items()])
            return list(set(_specific_gender_variants))
        else:
            return job_list

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        job_title = payload.query.get(self.job_title_field)
        if isinstance(job_title, str):
            try:
                semantic_expansion_jobs = self._get_semantic_expansion(payload, bearer_token=bearer_token)
                query = self._build(semantic_expansion_jobs)
                return QueryComponentResponse(
                    query=query,
                    response_data={"semanticExpansion": {"jobs": semantic_expansion_jobs}}
                )
            except RequestError:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _get_semantic_expansion(self, payload, bearer_token: str = None):
        job_title = payload.query.get(self.job_title_field).lower()
        _provided_semantic_expansion = self._set_provided_semantic_expansion(payload)

        if _provided_semantic_expansion.jobs is None:
            job_title_expansion = self._get_job_title_expansion(job_title, bearer_token=bearer_token)
            semantic_expansion_jobs = self._format_as_semantic_expansion(job_title_expansion)
        else:
            semantic_expansion_jobs = payload.query.get("semanticExpansion").jobs

        return semantic_expansion_jobs

    @staticmethod
    def _set_provided_semantic_expansion(payload: RequestPayload) -> SemanticExpansion:
        _provided_semantic_expansion = SemanticExpansion(jobs=None, skills=None)
        if payload.query.get("semanticExpansion") is not None:
            _provided_semantic_expansion = payload.query.get("semanticExpansion", SemanticExpansion(jobs=None, skills=None))
        return _provided_semantic_expansion

    def _get_job_title_expansion(self, job_title, bearer_token: str = None):
        job_title_expansion = None
        if self.curated_jobs_expansion:
            job_title_expansion = self._fetch_curated_job_title_expansion(job_title)

        if job_title_expansion is None:
            job_title_expansion = self.job2jobs_service(job_title, bearer_token=bearer_token).keys()

        return self._remove_original_job_title(job_title, job_title_expansion)

    def _fetch_curated_job_title_expansion(self, job_title):
        for key, data in self.curated_jobs_expansion.items():
            if job_title in data["specific"]:
                return data["neutral"]
        return None

    def _remove_original_job_title(self, job_title, job_list):
        _gender_variants = self._get_gender_variants(job_title)
        _gender_variants = [v["jobTitle"] for k, v in _gender_variants.items()]
        return [j for j in job_list if j not in _gender_variants]

    @staticmethod
    def _format_as_semantic_expansion(job_list: List[str]) -> List[dict]:
        return [{"name": j, "isChecked": True} for j in job_list]

    def _build(self, semantic_expansion_jobs: List[dict]) -> dict:
        _match_phrase_queries = self._build_match_queries(semantic_expansion_jobs)

        if _match_phrase_queries:
            return wrap_bool_query(self._build_valid(_match_phrase_queries), bool_type=self.bool_type)
        else:
            return {}

    def _build_valid(self, _match_phrase_queries: list) -> dict:
        return query_dict("bool",
                 should=_match_phrase_queries,
                 _name=self.name
                 )

    def _build_match_queries(self, semantic_expansion_jobs: List[dict]) -> List[Dict[str, Any]]:
        _match_phrase_queries = []
        for expansion in semantic_expansion_jobs:
            if expansion["isChecked"]:
                _match_phrase_queries.extend(self._get_job_query_variants(expansion["name"]))
        return _match_phrase_queries
