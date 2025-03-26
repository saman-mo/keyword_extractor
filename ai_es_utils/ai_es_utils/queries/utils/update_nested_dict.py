import copy
import warnings


class OverrideValueWarning(Warning):
    """
    When update nested dicts and both hold the same key with different value it is not
    immediately clear which value should be kept. If possible, refactor your code such
    that no overwriting is required.
    """
    pass


def update_nested_dict(input_dict: dict, source_dict: dict) -> dict:
    """
    Combines two arbitrarily deeply nested dictionaries, i.e. this function is called
    recursively on all sub-dictionaries of the original dictionary. Lists contained in
    both dictionaries are _safely_ extended, whereas other non-dict and non-list values
    are *overwritten* with that of the input dict! This behaviour is indicated by a
    `OverrideValueWarning` and should be avoided if possible, as it can lead to confusing
    behavior, which is hard to debug.

    :param input_dict: nested dictionary with new content
    :param source_dict: nested dictionary acting as the base to update
    :return: combined dictionary
    """

    output_dict = copy.deepcopy(source_dict)
    for key, value in input_dict.items():
        if key in output_dict:
            if isinstance(output_dict[key], dict):
                assert isinstance(value, dict)
                output_dict[key] = update_nested_dict(value, output_dict[key])
            elif isinstance(output_dict[key], list):
                assert isinstance(value, list)
                output_dict[key].extend(value)
            else:
                if output_dict[key] != value:
                    warnings.warn(
                        f"""Warning: Override {output_dict[key]} with {value} for key {key}. 
                        This is ill-defined and can lead to unintended behavior.""",
                        category=OverrideValueWarning
                    )
                    output_dict[key] = value
        else:
            output_dict[key] = value
    return output_dict
