ELASTICSEARCH_RESERVED_CHARS = '+,-,=,&&,||,>,<,!,(,),{,},[,],^,",~,*,?,:,\\,/'.split(",")
RESERVED_CHAR_MAP = {c: "".join(["\\" + _c for _c in c]) for c in ELASTICSEARCH_RESERVED_CHARS}


def escape_reserved_characters(term):  # TODO Write test for this function
    if "\\" in ELASTICSEARCH_RESERVED_CHARS:
        term = term.replace("\\", RESERVED_CHAR_MAP.get("\\"))
    for c in ELASTICSEARCH_RESERVED_CHARS:
        if c != "\\":
            term = term.replace(c, RESERVED_CHAR_MAP.get(c))
    return term


def build_query_string_phrase(term: str, fuzzy=True):
    sub_terms = term.strip().split(" ")
    if fuzzy:
        sub_terms = [escape_reserved_characters(term) + "~" for term in sub_terms]
    else:
        sub_terms = [escape_reserved_characters(term) for term in sub_terms]
    return f'({" ".join(sub_terms)})'


def generate_query_string(term_list: list, fuzzy=True) -> str:
    term_list = [build_query_string_phrase(term, fuzzy=fuzzy) for term in term_list]
    return " OR ".join(term_list)
