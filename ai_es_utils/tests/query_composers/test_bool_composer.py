import pytest

from ai_es_utils.queries.composers.bool_composer import BoolQueryComposer
from ai_es_utils.queries.utils import query_dict


@pytest.mark.parametrize(
    "query_list, expected_query", [
        # Basic merge of inner bool.should queries
        (
                [
                    {"query": query_dict("bool", must=[query_dict("bool", should=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool",
                                         must=[query_dict("bool", should=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool",
                                     must=[query_dict("bool",
                                                      should=[
                                                          query_dict("match", key="value"),
                                                          query_dict("match", key2="value2")
                                                      ])])

                 }
        ),
        # Do not merge "not-should" queries
        (
                [
                    {"query": query_dict("bool", must=[query_dict("bool", must=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool", must=[query_dict("bool", must=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool", must=[
                    query_dict("bool", must=[query_dict("match", key="value")]),
                    query_dict("bool", must=[query_dict("match", key2="value2")])
                ])}
        ),
        (
                [
                    {"query": query_dict("bool", must=[query_dict("bool", filter=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool",
                                         must=[query_dict("bool", filter=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool", must=[
                    query_dict("bool", filter=[query_dict("match", key="value")]),
                    query_dict("bool", filter=[query_dict("match", key2="value2")])
                ])}
        ),
        (
                [
                    {"query": query_dict("bool",
                                         must=[query_dict("bool", must_not=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool",
                                         must=[query_dict("bool", must_not=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool", must=[
                    query_dict("bool", must_not=[query_dict("match", key="value")]),
                    query_dict("bool", must_not=[query_dict("match", key2="value2")])
                ])}
        ),
        # Do not merge unsupported bool-keys
        (
                [
                    {"query": query_dict("bool",
                                         unsupported=[query_dict("bool", should=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool",
                                         unsupported=[query_dict("bool", should=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool",
                                     unsupported=[
                                         query_dict("bool", should=[query_dict("match", key="value")]),
                                         query_dict("bool", should=[query_dict("match", key2="value2")])
                                     ])}
        )
    ]
)
def test_sub_query_composition(query_list, expected_query):
    bool_composer = BoolQueryComposer()
    assert bool_composer(query_list) == expected_query


@pytest.mark.parametrize(
    "minimum_should_match, query_list, expected_query", [
        (
                2,
                [
                    {"query": query_dict("bool", must=[query_dict("bool", should=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool",
                                         must=[query_dict("bool", should=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool",
                                     must=[query_dict("bool",
                                                      should=[
                                                          query_dict("match", key="value"),
                                                          query_dict("match", key2="value2")
                                                      ],
                                                      minimum_should_match=2)])}
        ),
        (
                None,
                [
                    {"query": query_dict("bool", must=[query_dict("bool", should=[query_dict("match", key="value")])])},
                    {"query": query_dict("bool",
                                         must=[query_dict("bool", should=[query_dict("match", key2="value2")])])}
                ],
                {"query": query_dict("bool",
                                     must=[query_dict("bool",
                                                      should=[
                                                          query_dict("match", key="value"),
                                                          query_dict("match", key2="value2")
                                                      ])])}
        ),
    ]
)
def test_minimum_should_match_injection(minimum_should_match, query_list, expected_query):
    bool_composer = BoolQueryComposer(minimum_should_match=minimum_should_match)
    assert bool_composer(query_list) == expected_query
