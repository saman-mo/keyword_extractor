from typing import List, Dict, Any

from ai_es_utils.queries.composers.group_by_name_composer import GroupByNameComposer
from ai_es_utils.queries.utils import query_dict


class FunctionScoreGroupComposer(GroupByNameComposer):
    def __init__(self, function_list: List[Dict[str, Any]], **kwargs):
        super().__init__(**kwargs)
        self.function_list = function_list

    def __call__(self, query_stack: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        self._query = super().__call__(query_stack, **kwargs)
        self._query["query"] = query_dict(
            "function_score",
            functions=self.function_list,
            query=self._query["query"]
        )
        return self._query
