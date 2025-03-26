from typing import Union, List, Dict, Any

from ai_es_utils.queries.utils.query_dict import query_dict


def wrap_bool_query(queries: Union[Dict[str, Any], List[Dict[str, Any]]], bool_type: str = None) -> Dict[str, Any]:
    if not isinstance(queries, list):
        queries = [queries]
    return {
        "query": query_dict("bool", **{bool_type: queries})
    }
