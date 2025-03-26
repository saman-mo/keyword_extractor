from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai_es_utils.queries.models.payload import RequestPayload


@dataclass
class QueryComponentResponse:
    query: dict
    response_data: dict = field(default_factory=dict)


class QueryComponent(ABC):
    """
    Query components implement a self-sufficient elasticsearch query
    with a single responsibility, such as searching for a match on a
    list of skills. Each component should be easy to test in
    isolation.

    To build more complex queries, feed the desired components to a
    query composer.
    """

    @abstractmethod
    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        """
        Builds self-sufficient elasticsearch query from the search request
        payload. This method is called by the composer to gather all
        components and combine them into a single complex query.

        :param bearer_token: hand down bearer token for expanding queries
        :param payload: search request payload
        :return: response holding a self-sufficient elasticsearch query as well as optional response data.
        """
        return QueryComponentResponse(query=dict())
