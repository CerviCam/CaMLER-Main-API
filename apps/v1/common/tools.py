def set_prefix_to_key_on_dict(prefix, dict_data):
    new_dict_data = dict()
    for key in dict_data.keys():
        new_dict_data[prefix + key] = dict_data[key]

    return new_dict_data