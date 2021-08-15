from env.environment import PortfolioEnv
from agents.agent_ppo import Agent
from plot import add_curve, save_plot


def main():
    figure_file = 'plots/ppo.png'

    env = PortfolioEnv(action_scale=1000)
    djia_history = env.get_djia_history()
    add_curve(djia_history/djia_history[0], 'DJIA')

    T = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=env.n_actions(), batch_size=batch_size, alpha=alpha,
                  n_epochs=n_epochs, input_dims=env.state_shape(),
                  fc1_dims=512, fc2_dims=512)

    # agent.load_models()

    score_history = []
    djia = []

    learn_iters = 0
    n_steps = 0

    observation = env.reset()
    djia_initial = sum(observation[1:31])
    done = False
    while not done:
        action, prob, val = agent.choose_action(observation)
        observation_, reward, done, info, wealth = env.step(action)
        n_steps += 1
        agent.remember(observation, action, prob, val, reward, done)
        if n_steps % T == 0:
            agent.learn()
            learn_iters += 1
        observation = observation_
        print(f"Date: {info},\tBalance: {int(observation[0])},\tWealth: {int(wealth)},\t"
              f"Shares: {observation[31:61]}")
        score_history.append(wealth/1000000)
        djia.append(sum(observation[1:31])/djia_initial)

    agent.save_models()

    add_curve(score_history, 'PPO')
    save_plot(figure_file)


if __name__ == '__main__':
    main()
