import numpy as np
import torch as T
from agents.agent_a2c import ActorCritic
from agents.agent_a2c import Agent

N_AGENTS = 16
GAMMA = 0.99
LEARNING_R = 1e-3
BETAS = (0.92, 0.999)
EPS = 1e-8
W_DECAY = 0
T_MAX = 5


def main():

    global_actor_critic = ActorCritic(input_dims=(61,), n_actions=30, layer1_size=128, layer2_size=128)
    optimizer = T.optim.Adam(global_actor_critic.parameters())

    workers = [Agent(global_actor_critic,
                     input_dims=(61,),
                     n_actions=30,
                     gamma=GAMMA,
                     name=i,
                     t_max=T_MAX,
                     layer1_size=128,
                     layer2_size=128) for i in range(N_AGENTS)]

    while Agent.n_dones < N_AGENTS:
        [w.iterate() for w in workers]
        if Agent.n_gradients == N_AGENTS:
            gradients = np.array([w.get_gradient() for w in workers], dtype=object)
            mean_gradient = np.mean(gradients, axis=0)
            for grad, global_param in zip(
                    mean_gradient,
                    global_actor_critic.parameters()):
                global_param._grad = grad
            optimizer.step()
            [w.resume() for w in workers]
            # print("------ global network updated ------")


if __name__ == '__main__':
    main()
