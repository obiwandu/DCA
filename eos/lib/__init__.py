import copy


def model_to_dict(obj):
    result  = copy.deepcopy(obj.__dict__)
    del result['_state']
    return result