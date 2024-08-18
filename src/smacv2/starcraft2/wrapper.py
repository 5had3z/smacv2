from smacv2.starcraft2.distributions import get_distribution
from smacv2.starcraft2.starcraft2 import CannotResetException, StarCraft2Env


class StarCraftCapabilityEnvWrapper(StarCraft2Env):
    def __init__(self, **kwargs):
        self.distribution_config = kwargs["capability_config"]
        self.env_key_to_distribution_map = {}
        self._parse_distribution_config()
        super().__init__(**kwargs)
        assert (
            self.distribution_config.keys()
            == kwargs["capability_config"].keys()
        ), "Must give distribution config and capability config the same keys"

    def _parse_distribution_config(self):
        for env_key, config in self.distribution_config.items():
            if env_key in {"n_units", "n_enemies"}:
                continue
            config["env_key"] = env_key
            # add n_units key
            config["n_units"] = self.distribution_config["n_units"]
            config["n_enemies"] = self.distribution_config["n_enemies"]
            distribution = get_distribution(config["dist_type"])(config)
            self.env_key_to_distribution_map[env_key] = distribution

    def reset(self):
        try:
            reset_config = {}
            for distribution in self.env_key_to_distribution_map.values():
                reset_config = {**reset_config, **distribution.generate()}
            return super().reset(reset_config)
        except CannotResetException:
            # just retry
            return self.reset()
