from typing import Dict, Any

from ai_es_utils.queries.composers.group_by_name_composer import GroupByNameComposer, List
from ai_es_utils.queries.utils import query_dict


class DecayLastScrapedGroupedComposer(GroupByNameComposer):
    def __init__(
            self,
            decay=0.3,
            offset="30d",
            origin="now",
            scale="90d",
            **kwargs
    ):
        super().__init__(**kwargs)
        self.decay = decay
        self.offset = offset
        self.origin = origin
        self.scale = scale

    def __call__(self, query_stack: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        self._query = super().__call__(query_stack, **kwargs)
        self._query["query"] = query_dict(
            "function_score",
            functions=[self._get_decay_function()],
            query=self._query["query"]
        )

        return self._query

    def _get_decay_function(self) -> Dict[str, Any]:
        return {
            "gauss": {
                "lastScraped": {
                    "decay": self.decay,
                    "offset": self.offset,
                    "origin": self.origin,
                    "scale": self.scale
                }
            }
        }
