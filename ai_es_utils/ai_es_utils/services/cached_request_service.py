from abc import ABC

import requests_cache
from requests_cache import Response

from ai_es_utils.services.exceptions import RequestError


class CachedRequestService(ABC):
    def __init__(self, **kwargs):
        self.request_session = requests_cache.CachedSession("memory", **kwargs)

    def _get(self, *args, **kwargs) -> Response:
        response = self.request_session.get(*args, **kwargs)
        if response.status_code not in [200, 204]:
            raise RequestError(
                f"Request failed with status code {response.status_code}. error: {response.text}"
            )
        return response
