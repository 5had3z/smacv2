from smacv2.starcraft2.maps import smac_maps


def get_map_params(map_name):
    map_param_registry = smac_maps.get_smac_map_registry()
    return map_param_registry[map_name]
