import json
from typing import Dict

from ai_es_utils.search.highlight_replacer import HighlightReplacer


def assert_get(_dict: dict, key: str):
    assert key in _dict, f"{key} not in {json.dumps(_dict)}"
    return _dict.get(key)


class SearchResultProcessor:
    """
    A class that executes post-processing of search results preparing the response for the frontend.
    """

    def __init__(self,
                 include_relevance=True,
                 highlight_replacer: HighlightReplacer = HighlightReplacer()):
        self.include_relevance = include_relevance
        self.highlight_replacer = highlight_replacer

        self.max_total_count = 9_990
        self.max_score = None

    def __call__(
            self,
            results: Dict,
            **kwargs
    ):
        """
        Apply post processing to elastic search results, i.e. extract and reformat profiles,
        return max score, and inject hand-down `kwargs`.

        :param results: Plain response from elasticsearch query.
        :param kwargs: Hand-down entries for the search response
        :return:
        """
        # Fetch results:
        results = assert_get(results, "hits")

        # Check valid results
        instance_count = self._get_instance_count(results)
        self.max_score = results.get("max_score")
        assert (instance_count > 0 and self.max_score is not None) or instance_count == 0

        # Fetch profiles:
        profiles = assert_get(results, "hits")
        processed_profiles = [self._process_profiles(p) for p in profiles]

        # Build response:
        response = dict()
        response["profileInstanceList"] = processed_profiles
        response["profileInstanceCount"] = instance_count
        # Insert hand-down entries
        response.update(kwargs)

        return response

    def _get_instance_count(self, results):
        try:
            total = results["total"]
            if isinstance(total, int):
                return min([total, self.max_total_count])
            elif isinstance(total, dict):
                return min([total["value"], self.max_total_count])
        except KeyError:
            pass
        return self.max_total_count

    def _process_profiles(self, profile):
        processed_profile = assert_get(profile, "_source")
        if "highlight" in profile:
            processed_profile = self._apply_highlighting(processed_profile, profile["highlight"])
        processed_profile["_id"] = assert_get(profile, "_id")

        if self.include_relevance:
            processed_profile["relevance"] = self._get_relevance_from_score(assert_get(profile, "_score"))

        return processed_profile

    def _apply_highlighting(self, profile: dict, highlight_dict: dict) -> dict:
        self.highlight_replacer.build(highlight_dict)
        return self.highlight_replacer(profile)

    def _get_relevance_from_score(self, score):
        return max(int((score / self.max_score) * 100), 1)


if __name__ == "__main__":
    with open("../../tests/test_data/search_results/full_search_result.json", "r") as file:
        search_result = json.load(file)

    post_processor = SearchResultProcessor()

    _response = post_processor(search_result, location={"lat": 52.51704, "lon": 13.38886})
    print(json.dumps(_response))
