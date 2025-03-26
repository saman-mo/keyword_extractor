import json
import logging
from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComposer
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import update_nested_dict
from ai_es_utils.search import SearchResultProcessor
from ai_es_utils.services import ElasticSearchService


class SearchExecutor:
    def __init__(
            self,
            elasticsearch: ElasticSearchService,
            query_stack: List[QueryComponent] = None,
            query_composer: QueryComposer = None,
            post_processor: SearchResultProcessor = SearchResultProcessor(),
            verbose: int = 0
    ):
        """
        Orchestrates the whole search from start to finish. In particular, the request payload
        is passed to all query components of the `query_stack`. Next the resulting sub-queries
        are fed into the `query_compose` to formulate a single, final query. Finally, the
        search is fired and the results, as well as response data provided by the query components
        are written and formatted by the `post_processor`.

        :param elasticsearch: ElasticSearchService that handles the request to elasticsearch
        :param query_stack: List of QueryComponents that define the search logic
        :param query_composer: QueryComposer which build the final query from the sub-queries provided by the query components
        :param post_processor: SearchResultProcessor which formats the results, and injects response data into the response
        :param verbose: int indicating the level of verbosity
        """

        self.elasticsearch = elasticsearch
        self.query_stack = query_stack
        self.query_composer = query_composer
        self.post_processor = post_processor
        self.verbose = verbose

    def __call__(self, payload: RequestPayload, bearer_token: str = None, **kwargs):
        """
        Is called to execute a search. This requires a valid payload, as well as a valid bearer token
        that is included in the initial request. Additional keyword arguments are passed directly to
        the `self.post_processor` and can be included in the resulting response.

        :param payload: RequestPayload
        :param bearer_token: Bearer Token from authentication
        :param kwargs: Additional keyword arguments passed to post_processor
        :return:
        """
        query, response_data = self._build_query(payload, bearer_token=bearer_token)
        results = self._execute_search(query)
        return self._format_results(results, response_data, **kwargs)

    def _build_query(self, payload: RequestPayload, bearer_token: str = None) -> (dict, dict):
        queries = []
        response_data = {}
        for query_component in self.query_stack:
            response = query_component.query(payload, bearer_token=bearer_token)
            queries.append(response.query)
            response_data = update_nested_dict(response.response_data, response_data)

        return self.query_composer(queries), response_data

    def _execute_search(self, query):
        if self.verbose > 0:
            logging.info(json.dumps(query))

        results = self.elasticsearch.execute(query)

        if self.verbose > 1:
            logging.info(json.dumps(results))

        return results

    def _format_results(self, results: dict, response_data: dict, **kwargs):
        return self.post_processor(results, **response_data, **kwargs)
