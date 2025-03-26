"""Client to request skills for a given job from job2skills service"""
from typing import Dict
from urllib.parse import urlencode

from requests_cache import Response

from ai_es_utils.services import CachedRequestService


class InternalJob2SkillsService(CachedRequestService):
    def __init__(self,
                 endpoint_url: str,
                 topn: int = 10,
                 backend: str = "memory",
                 expire_after: int = 20,
                 upper_threshold: float = None,
                 lower_threshold: float = None,
                 **kwargs):
        """
        Service that fetches skills related to a provided job title. The request is cached to improve performance
        for subsequent calls.

        :param endpoint_url: endpoint of the job2skill model
        :param topn: maximum number of skills to be served
        :param backend: cache storage; passed to CachedSession, defaults to memory
        :param expire_after: number of seconds when the cache expires, defaults to 20
        :param kwargs: keyword arguments passed to cached request session
        """
        self._url = endpoint_url
        self._topn = topn
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        super().__init__(
            backend=backend,
            expire_after=expire_after,
            **kwargs
        )

    def __call__(self, job_title: str, bearer_token: str = None, **kwargs) -> Dict[dict, float]:
        url = self._build_url(job_title)
        response = self._get(url, **kwargs)
        return self._process_response(response)

    def _build_url(self, job_title: str) -> str:
        args = urlencode({'jobTitle': job_title.lower(), 'topn': self._topn})
        return f"{self._url}?{args}"

    def _process_response(self, response: Response) -> dict:
        suggestions = {}
        if response.status_code == 200:
            suggestions = response.json()
        suggestions = {k: v for k, v in suggestions.items() if self._satisfies_thresholds(v)}
        return suggestions

    def _satisfies_thresholds(self, value: float) -> bool:
        if isinstance(self.upper_threshold, float):
            if value > self.upper_threshold:
                return False
        if isinstance(self.lower_threshold, float):
            if value < self.lower_threshold:
                return False
        return True
