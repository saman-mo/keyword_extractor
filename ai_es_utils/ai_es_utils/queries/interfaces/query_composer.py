from abc import ABC, abstractmethod
from typing import List


class QueryComposer(ABC):
    def __init__(self, **kwargs):
        """
        The query composer orchestrates the building of the final query. It takes a list of
        query components, which defines the type of search that is performed. Calling the
        `build` method, all sub queries are build for the provided payload and the composer
        is responsible to combine them into a well defined final query.

        The query composer takes a list of dicts, containing sub queries, and combines them
        into a single elasticsearch query.

        :param kwargs: keyword arguments passed to the final query in the highest level
        """
        self._query = None
        self.kwargs = kwargs

    def reset(self):
        """
        Initializes the final query to an empty dict.

        :return:
        """
        self._query = dict()

    @abstractmethod
    def __call__(self, query_stack: List[dict], **kwargs) -> dict:
        """
        Combines sub-query in to a single elasticsearch query.

        :param query_stack: ist of sub-queries to combine
        :param kwargs: dictionary directly updating the final query
        :return: composed query as dict
        """
        pass
