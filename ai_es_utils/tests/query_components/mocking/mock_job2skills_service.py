from typing import Dict

from ai_es_utils.services.enrichment.job2skills_client import Job2SkillsService
from ai_es_utils.services.exceptions import RequestError


class MockJob2SkillsService(Job2SkillsService):
    def __init__(self, mock_data: dict):
        super().__init__("mock.url")
        self.mock_data = mock_data

    def __call__(self, job_title: str, bearer_token: str) -> Dict[dict, float]:
        if bearer_token != "valid token":
            raise RequestError()
        return self.mock_data.get(job_title, {})

