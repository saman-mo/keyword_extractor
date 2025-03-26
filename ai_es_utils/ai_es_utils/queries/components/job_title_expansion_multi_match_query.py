from typing import List, Dict, Any

from ai_es_utils.queries.components.job_title_expansion_query import JobTitleExpansionQuery
from ai_es_utils.services.enrichment import Job2JobsService
from ai_es_utils.queries.utils import query_dict


class JobTitleExpansionMultiMatchQuery(JobTitleExpansionQuery):
    def __init__(
            self,
            job2jobs_service: Job2JobsService,
            boosted_fields: List[str] = None,
            gender_normalization_map: dict = None,
            curated_jobs_expansion: dict = None,
            name: str = "job_title_expansion",
            nested_bool: bool = False,
            multi_match_type: str = "phrase",
            job_title_field: str = "jobTitle",
            bool_type: str = "must",
            boost_factor: float = None,
            **kwargs
    ):
        """
        Same as base `JobTitleExpansionQuery`, searching on similar job titles ot the original job title.
        Main feature is to group each term under a multi_match query, which covers multiple fields at once.

        :param job2jobs_service: service serving similar jobs to the query job
        :param boosted_fields: list of fields in boosted format, e.g. "field^2.0"
        :param gender_normalization_map: dictionary mapping from neutral job titles to all known gender variants
        :param curated_jobs_expansion: dictionary holding curated list of jobs to serve for certain job titles
        :param name: name of the query group
        :param nested_bool: controls if fields should be considered nested or flat (e.g. "jobs.jobTitle")
        :param multi_match_type: elasticsearch option multi_match -> type
        :param job_title_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match_phrase query
        """

        if nested_bool:
            raise NotImplementedError(
                "Since new ES index is not nested 'nested_bool=True' feature has not been implemented yet!"
            )

        super().__init__(
            job2jobs_service=job2jobs_service,
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

        self.multi_match_type = multi_match_type

    def _get_job_query_variants(self, job_title) -> List[Dict[str, Any]]:
        gender_variants = self._get_gender_variants(job_title)
        sub_queries = [self._build_multi_match_query(specific_gender["jobTitle"])
                       for gender, specific_gender in gender_variants.items()
                       if gender in ["male", "female"]]
        return sub_queries

    def _build_multi_match_query(self, job_title: str) -> Dict[str, Any]:
        return query_dict("multi_match",
                 query=job_title,
                 fields=list(self.boosted_fields),
                 _name=f"{self.name}.{job_title}",
                 type=self.multi_match_type,
                 **self.kwargs)
