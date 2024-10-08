#!/usr/bin/env python3

from pysc2 import maps as pysc2_maps

from smacv2.starcraft2.maps import smac_maps


def main():
    smac_map_registry = smac_maps.get_smac_map_registry()
    all_maps = pysc2_maps.get_maps()
    print("{:<15} {:7} {:7} {:7}".format("Name", "Agents", "Enemies", "Limit"))
    for map_name, map_params in smac_map_registry.items():
        map_class = all_maps[map_name]
        if map_class.path:
            print(
                "{:<15} {:<7} {:<7} {:<7}".format(
                    map_name,
                    map_params["n_agents"],
                    map_params["n_enemies"],
                    map_params["limit"],
                )
            )


if __name__ == "__main__":
    main()
