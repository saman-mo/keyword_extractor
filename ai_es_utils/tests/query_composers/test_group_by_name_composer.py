import pytest

from ai_es_utils.queries.composers import GroupByNameComposer
from ai_es_utils.queries.utils import query_dict


@pytest.mark.parametrize(
    "query_list, expected_query", [
        # Group queries only if they share the same name
        (
                [
                    {"query": query_dict("bool", must=[
                        query_dict("bool", should=[query_dict("match", key="value1")], _name="group1")])},
                    {"query": query_dict("bool", must=[
                        query_dict("bool", should=[query_dict("match", key="value2")], _name="group1")])},
                    {"query": query_dict("bool", must=[
                        query_dict("bool", should=[query_dict("match", key="valueA")], _name="group2")])},
                    {"query": query_dict("bool", must=[
                        query_dict("bool", should=[query_dict("match", key="valueB")], _name="group2")])},
                    {"query": query_dict("bool", must=[query_dict("bool", should=[query_dict("match", key="unique")])])}
                ],
                {"query": query_dict("bool", must=[
                    query_dict("bool", should=[query_dict("match", key="unique")]),
                    query_dict("bool", should=[
                        query_dict("match", key="value1"),
                        query_dict("match", key="value2")
                    ], _name="group1"),
                    query_dict("bool", should=[
                        query_dict("match", key="valueA"),
                        query_dict("match", key="valueB")
                    ], _name="group2")
                ])}
        ),
        # Only group queries if they are under the same top-level bool query
        (
                [
                    {"query": query_dict("bool", must=[
                        query_dict("bool", should=[query_dict("match", key="value1")], _name="group1")])},
                    {"query": query_dict("bool", must=[
                        query_dict("bool", should=[query_dict("match", key="value2")], _name="group1")])},
                    {"query": query_dict("bool",
                                         must_not=[query_dict("bool", should=[query_dict("match", key="valueA")],
                                                              _name="group1")])},
                    {"query": query_dict("bool",
                                         must_not=[query_dict("bool", should=[query_dict("match", key="valueB")],
                                                              _name="group1")])},
                ],
                {"query": query_dict("bool",
                                     must=[
                                         query_dict("bool", should=[
                                             query_dict("match", key="value1"),
                                             query_dict("match", key="value2")
                                         ], _name="group1")
                                     ],
                                     must_not=[
                                         query_dict("bool", should=[
                                             query_dict("match", key="valueA"),
                                             query_dict("match", key="valueB")
                                         ], _name="group1")
                                     ]
                                     )
                 }
        ),
    ]
)
def test_sub_query_composition(query_list, expected_query):
    group_by_name_composer = GroupByNameComposer()
    assert group_by_name_composer(query_list) == expected_query
