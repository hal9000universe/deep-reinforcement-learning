# py
import time
from typing import Callable, Tuple

# nn & rl
import gym
import jax
import haiku as hk
import optax
from numpy import ndarray

# lib
from Base.q_agent import Agent
from Base.utils import generate_loading, generate_visualization
from LunarLander.env import ObsWrapper
from LunarLander.dddqn import Model


if __name__ == '__main__':
    BATCH_SIZE: int = 32
    BUFFER_SIZE: int = 1000000
    MAX_STEPS: int = 2000
    MAX_EPISODES: int = 10000
    REPLACE_FREQUENCY: int = 25
    BACKUP_FREQUENCY: int = 50
    TRAINING_START: int = 256
    TRAIN_FREQUENCY: int = 4
    EPSILON: float = 1.0
    EPSILON_DECAY_RATE: float = 0.995
    MIN_EPSILON: float = 0.01
    GAMMA: float = 0.999
    LEARNING_RATE: float = 0.001
    REWARD_TO_REACH: float = 240.
    DIR: str = "lunar_lander"

    env: gym.Env = ObsWrapper(gym.make('LunarLander-v2'), MAX_STEPS)
    obs_shape: Tuple = (BUFFER_SIZE, 9)
    ac_shape: Tuple = (BUFFER_SIZE,)
    NUM_ACTIONS: int = env.action_space.n

    rng: jax.random.PRNGKeyArray = jax.random.PRNGKey(time.time_ns())
    test_input: ndarray = env.reset()

    model: hk.Transformed = hk.without_apply_rng(hk.transform(lambda *args: Model(NUM_ACTIONS)(*args)))
    optimizer: optax.adam = optax.adam(LEARNING_RATE)

    parameters: hk.Params = model.init(rng, test_input)
    optimizer_state = optimizer.init(parameters)

    agent = Agent(
        network=model,
        params=parameters,
        optimizer=optimizer,
        opt_state=optimizer_state,
        env=env,
        buffer_size=BUFFER_SIZE,
        obs_shape=obs_shape,
        ac_shape=ac_shape,
        gamma=GAMMA,
        epsilon=EPSILON,
        epsilon_decay_rate=EPSILON_DECAY_RATE,
        min_epsilon=MIN_EPSILON,
        max_episodes=MAX_EPISODES,
        max_steps=MAX_STEPS,
        training_start=TRAINING_START,
        batch_size=BATCH_SIZE,
        train_frequency=TRAIN_FREQUENCY,
        back_up_frequency=BACKUP_FREQUENCY,
        replace_frequency=REPLACE_FREQUENCY,
        reward_to_reach=REWARD_TO_REACH,
        num_actions=NUM_ACTIONS,
        saving_directory=DIR,
        timed=False,
    )
    agent.training()

    load_state: Callable = generate_loading(DIR)
    visualize: Callable = generate_visualization(env, model)

    parameters = load_state()
    for _ in range(10):
        visualize(parameters)
