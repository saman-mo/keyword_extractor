from typing import List, Dict, Any

from ai_es_utils.queries.components.job_title_query import JobTitleQuery
from ai_es_utils.queries.utils import build_field_path_map, generate_query_string, format_boosted_field, query_dict


class JobTitleBooleanQuery(JobTitleQuery):
    def __init__(self,
                 boosted_fields: List[str] = ("jobTitle^2.0", "previousJobTitles"),
                 gender_normalization_map: dict = None,
                 name: str = "job_title",
                 fuzzy: bool = True,
                 nested_bool: bool = False,
                 job_title_field: str = "jobTitle",
                 bool_type: str = "must",
                 boost_factor: float = None,
                 **kwargs):
        """
        The component produces a fuzzy query based on the job title. If a gender normalization map was provided, the job
        title is extended to its gender variants. The query is composed of multiple query_string queries combining all
        gender variants and searching in all requested fields.

        :param boosted_fields: list of fields in boosted format, e.g. "field^2.0"
        :param gender_normalization_map: dictionary mapping from neutral job titles to all known gender variants
        :param minimum_should_match: number of job titles that need to match, default is 1
        :param name: name of the query group
        :param nested_bool: controls if fields should be considered nested or flat (e.g. "jobs.jobTitle")
        :param job_title_field: field name in payload.query holding string
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match_phrase query
        """
        super().__init__(boosted_fields=boosted_fields,
                         gender_normalization_map=gender_normalization_map,
                         name=name,
                         nested_bool=nested_bool,
                         job_title_field=job_title_field,
                         bool_type=bool_type,
                         boost_factor=boost_factor,
                         **kwargs)

        self.field_path_map = None
        if self.nested_bool:
            self.field_path_map = build_field_path_map(self.fields, self.boosts)

        self.fuzzy = fuzzy

    def _get_job_query_variants(self, job_title) -> List[Dict[str, Any]]:
        gender_variants = self._get_gender_variants(job_title)
        normalized_job_title = gender_variants["normalized"]["jobTitle"]
        job_titles = [job["jobTitle"] for key, job in gender_variants.items() if key in ["male", "female"]]

        if self.nested_bool:
            return self._build_nested_subqueries(job_titles, normalized_job_title)
        else:
            sub_query_groups = [self._build_query_string_query(
                job_titles,
                [format_boosted_field(field, boost) for field, boost in zip(self.fields, self.boosts)],
                _name=f"{self.name}.{normalized_job_title}"
            )]
            return sub_query_groups

    def _build_nested_subqueries(self, job_titles: List[str], normalized_job_title: str) -> List[dict]:
        sub_query_groups = []
        for path, fields in self.field_path_map.items():
            if path == "None":
                sub_query_groups.append(
                    self._build_query_string_query(
                        job_titles,
                        fields,
                        _name=f"{self.name}.{normalized_job_title}"
                    )
                )
            else:
                sub_query_groups.append(
                    query_dict(
                        "nested",
                        path=path,
                        query=self._build_query_string_query(
                            job_titles,
                            [path + "." + field for field in fields]
                        ),
                        _name=f"{self.name}.{path}.{normalized_job_title}"
                    )
                )
        return sub_query_groups

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
