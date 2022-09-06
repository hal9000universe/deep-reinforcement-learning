# nn & rl
import gym
from numpy import ndarray, newaxis, float32


def transform(obs: ndarray) -> ndarray:
    obs = obs.__array__(float32)
    obs: ndarray = 0.3 * obs[:, :, :, 0] + 0.6 * obs[:, :, :, 1] + 0.1 * obs[:, :, :, 2]
    obs = obs[newaxis, ...]
    return obs


def create_env() -> gym.Env:
    env: gym.Env = gym.make('ALE/Breakout-v5',
                            full_action_space=False)
    env = gym.wrappers.FrameStack(env, 4)
    env = gym.wrappers.TransformObservation(env, transform)
    return env
