from collections import defaultdict

from ai_es_utils.queries.interfaces.query_composer import QueryComposer, List
from ai_es_utils.queries.utils import update_nested_dict


class GroupByNameComposer(QueryComposer):
    def __call__(self, query_stack: List[dict], **kwargs) -> dict:
        self.reset()
        for sub_query in query_stack:
            self._query = update_nested_dict(sub_query, self._query)

        self._query.update(kwargs)
        self._query.update(self.kwargs)
        self._contract_sub_query_lists_by_name()
        return self._query

    def _contract_sub_query_lists_by_name(self):
        for field in ["must", "must_not", "filter", "should"]:
            try:
                self._query["query"]["bool"][field] = self._contract_query_groups(self._query["query"]["bool"][field])
            except KeyError:
                pass

    @staticmethod
    def _contract_query_groups(sub_query_list: List[dict]) -> List[dict]:
        _query_groups = defaultdict(list)
        grouped_sub_query_list = []
        for sub_query in sub_query_list:
            try:
                _query_groups[sub_query["bool"]["_name"]].append(sub_query)
            except KeyError:
                grouped_sub_query_list.append(sub_query)

        for _, _list in _query_groups.items():
            tmp_query = dict()
            for q in _list:
                tmp_query = update_nested_dict(q, tmp_query)
            grouped_sub_query_list.append(tmp_query)
        return grouped_sub_query_list
