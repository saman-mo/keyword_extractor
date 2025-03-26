from typing import List

from ai_es_utils.queries.components.job_title_expansion_query import JobTitleExpansionQuery
from ai_es_utils.queries.utils import build_field_path_map, generate_query_string, format_boosted_field, \
    wrap_bool_query, query_dict
from ai_es_utils.services.enrichment import Job2JobsService


class JobTitleExpansionBooleanQuery(JobTitleExpansionQuery):
    def __init__(
            self,
            job2jobs_service: Job2JobsService,
            boosted_fields: List[str] = ("jobTitle^2.0", "previousJobTitles"),
            gender_normalization_map: dict = None,
            curated_jobs_expansion: dict = None,
            name: str = "job_title_expansion",
            fuzzy: bool = True,
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
        The query component returns response data that contains the semanticExpansions ``semanticExpansion.jobs``,
        allowing to track the user feedback, i.e. declining suggested job titles.If the payload already
        contains a valid semanticExpansion, these suggestions are used instead.

        In all cases, all jobs are expanded to all gender variants known, as provided by the
        `gender_normalization_map`.

        The kwargs are passed directly to the inner `query_string` query.

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
            job2jobs_service,
            boosted_fields=boosted_fields,
            gender_normalization_map=gender_normalization_map,
            curated_jobs_expansion=curated_jobs_expansion,
            name=name,
            nested_bool=nested_bool,
            job_title_field=job_title_field,
            bool_type=bool_type,
            boost_factor=boost_factor,
            **kwargs
        )
        self.field_path_map = None
        if self.nested_bool:
            self.field_path_map = build_field_path_map(self.fields, self.boosts)

        self.fuzzy = fuzzy

    def _build(self, semantic_expansion_jobs: List[dict]) -> dict:
        job_title_list = self._get_genderized_job_title_list(semantic_expansion_jobs)
        sub_queries = self._build_sub_queries(job_title_list)
        if sub_queries:
            return wrap_bool_query(self._build_valid(sub_queries), bool_type=self.bool_type)
        else:
            return {}

    def _get_genderized_job_title_list(self, semantic_expansion_jobs: List[dict]) -> list:
        title_list = []
        for expansion in semantic_expansion_jobs:
            if expansion["isChecked"]:
                gender_variants = self._get_gender_variants(expansion["name"])
                job_titles = [job["jobTitle"] for key, job in gender_variants.items() if key in ["male", "female"]]
                title_list.extend(job_titles)
        return title_list

    def _build_sub_queries(self, job_title_list: List[str]) -> list:
        if self.nested_bool:
            return self._build_nested_subqueries(job_title_list)
        else:
            return [self._build_query_string_query(
                job_title_list,
                [format_boosted_field(field, boost) for field, boost in zip(self.fields, self.boosts)],
                _name=f"{self.name}.expansion"
            )]

    def _build_nested_subqueries(self, job_titles: List[str]) -> List[dict]:
        sub_queries = []
        for path, fields in self.field_path_map.items():
            if path == "None":
                sub_queries.append(
                    self._build_query_string_query(
                        job_titles,
                        fields,
                        _name=f"{self.name}.expansion"
                    )
                )
            else:
                sub_queries.append(
                    query_dict(
                        "nested",
                        path=path,
                        query=self._build_query_string_query(
                            job_titles,
                            [path + "." + field for field in fields]
                        ),
                        _name=f"{self.name}.{path}.expansion"
                    )
                )
        return sub_queries

    def _build_query_string_query(self, job_titles: List[str], fields: List[str], **kwargs):
        return query_dict(
            "query_string",
            query=generate_query_string(job_titles, fuzzy=self.fuzzy),
            default_operator="AND",
            fuzziness="AUTO",
            auto_generate_synonyms_phrase_query=True,
            fields=fields,
            **kwargs,
            **self.kwargs
        )
