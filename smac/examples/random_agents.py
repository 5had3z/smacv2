from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from os import replace

from smac.env import StarCraft2Env
from smac.env.starcraft2.team_distributions import DISTRIBUTIONS
import numpy as np
from absl import logging
import time

logging.set_verbosity(logging.DEBUG)


# ally_train_teams = [
#     ["marine"] * 6 + ["marauder"] * 4,
#     ["marine"] * 10,
# ]
# ally_test_teams = [
#     ["marine"] * 4 + ["marauder"] * 3 + ["medivac"] * 3
# ]

# ally_train_teams = [["hydralisk"] * 10]
# ally_test_teams = [["zergling"] * 10]
ally_train_teams = [["stalker"] * 10, ["zealot"] * 10]
ally_test_teams = [["stalker"] * 5 + ["zealot"] * 5]


def main():
    env = StarCraft2Env(
        map_name="10gen_zerg",
        replace_teammates=True,
        teammate_train_distribution="all",
        teammate_test_distribution="all",
        ally_unit_types=["baneling", "zergling", "hydralisk"],
        n_units=6,
        mask_enemies=True,
    )
    # env.reset()

    env_info = env.get_env_info()

    n_actions = env_info["n_actions"]
    n_agents = env_info["n_agents"]
    cap_size = env_info["cap_shape"]

    n_episodes = 5

    print("Training episodes")
    for e in range(n_episodes):
        env.reset()
        terminated = False
        episode_reward = 0

        while not terminated:
            obs = env.get_obs()
            state = env.get_state()
            cap = env.get_capabilities()
            # env.render()  # Uncomment for rendering

            actions = []
            for agent_id in range(n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                actions.append(action)

            reward, terminated, _ = env.step(actions)
            time.sleep(0.15)
            episode_reward += reward

        # print("Total reward in episode {} = {}".format(e, episode_reward))

    print("Testing episodes")
    for e in range(n_episodes):
        env.reset(test_mode=True)
        terminated = False
        episode_reward = 0

        while not terminated:
            obs = env.get_obs()
            state = env.get_state()
            cap = env.get_capabilities()
            # env.render()  # Uncomment for rendering

            actions = []
            for agent_id in range(n_agents):
                avail_actions = env.get_avail_agent_actions(agent_id)
                avail_actions_ind = np.nonzero(avail_actions)[0]
                action = np.random.choice(avail_actions_ind)
                actions.append(action)

            reward, terminated, _ = env.step(actions)
            time.sleep(0.15)
            episode_reward += reward

        # print("Total reward in episode {} = {}".format(e, episode_reward))

    env.close()


if __name__ == "__main__":
    main()
