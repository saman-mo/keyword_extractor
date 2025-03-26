"""Client to request similar jobs for a given job from job2jobs service"""
from typing import Dict
from urllib.parse import urlencode

from requests_cache import Response

from ai_es_utils.services import CachedRequestService


class InternalJob2JobsService(CachedRequestService):
    def __init__(self,
                 endpoint_url: str,
                 thresh: float = 0.7,
                 topn: int = 20,
                 backend: str = "memory",
                 expire_after: int = 20,
                 **kwargs):
        """
        Service that fetches similar job titles for a provided job title. The request is cached
        to improve performance for subsequent calls.

        :param endpoint_url: url of 'job2jobs' endpoint serving suggestions
        :param thresh: minimum similarity score for similar jobs
        :param topn: maximum number of similar jobs to be served
        :param backend: cache storage; passed to CachedSession, defaults to memory
        :param expire_after: number of seconds when the cache expires, defaults to 20
        :param kwargs: keyword arguments passed to cached request session
        """
        self._url = endpoint_url
        self._thresh = thresh
        self._topn = topn + 1
        super().__init__(
            backend=backend,
            expire_after=expire_after,
            **kwargs
        )

    def __call__(self, job_title: str, bearer_token: str = None, **kwargs) -> Dict[dict, float]:
        """
        Serves suggestions for similar job titles compared ot the provided `job_title`.
        The authorization header can in principle be used to add authorization.

        :param job_title: job title to fetch similar job titles from.
        :param headers: headers passed to the get call
        :return:
        """
        url = self._build_url(job_title)
        response = self._get(url, **kwargs)
        return self._process_response(response, original_job_title=job_title.lower())

    def _build_url(self, job_title: str) -> str:
        args = urlencode({'jobTitle': job_title.lower(), 'topn': self._topn})
        return f"{self._url}?{args}"

    def _process_response(self, response: Response, original_job_title: str = None) -> dict:
        suggestions = {}
        if response.status_code == 200:
            suggestions = response.json()
        suggestions = {
            k: v for k, v in suggestions.items() if v > self._thresh and k != original_job_title
        }
        return suggestions
