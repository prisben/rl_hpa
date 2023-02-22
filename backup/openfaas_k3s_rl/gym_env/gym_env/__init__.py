from gym.envs.registration import register

register(
    id='gym_env',
    entry_point='gym_env.envs:GymEnv',
)