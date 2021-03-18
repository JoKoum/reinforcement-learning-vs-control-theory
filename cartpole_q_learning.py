import numpy as np
import math
import matplotlib.pyplot as plt
import gym

class Agent:
    '''A class to define an agent learning to control the system'''
    def __init__(self, environment, buckets = (3, 3, 6, 6), alpha=0.09,gamma=0.95):
        if not (0 < gamma <= 1):
            raise ValueError("Must be 0 < γ <= 1")
        self.alpha = alpha
        self.gamma = gamma
        self.environment = environment
        self.buckets = buckets
        self.upper_bounds = [self.environment.observation_space.high[0], 0.5, self.environment.observation_space.high[2], math.radians(50)]
        self.lower_bounds = [self.environment.observation_space.low[0], -0.5, self.environment.observation_space.low[2], -math.radians(50)]
        self.Q = np.zeros(self.buckets + (self.environment.action_space.n,))
        self.state = (0, 0, 0, 0)
        self.total_reward = 0

    def discretize(self, observations):
        '''Dicretize obervations based on the buckets'''
        discretized = []
        for i in range(len(observations)):
            scaling = ((observations[i] + np.abs(self.lower_bounds[i])) / (self.upper_bounds[i] - self.lower_bounds[i]))
            scaled_observations = int(round((self.buckets[i] - 1) * scaling))
            scaled_observations = min(self.buckets[i]- 1, max(0, scaled_observations))
            discretized.append(scaled_observations)
        return tuple(discretized)

    def choice(self):
        '''Randomly select among the two actions'''
        random_action = self.environment.action_space.sample()
        return random_action

    def greedy_action(self):
        '''Select action that has returned maximum reward'''
        return np.argmax(self.Q[self.state])
        

    def get_reward(self,action,state,reward):
        '''Update Q-value according to the state action pair'''
        self.total_reward += reward
        self.Q[self.state][action] = self.Q[self.state][action] + self.alpha * (reward + self.gamma * np.max(self.Q[state]) - self.Q[self.state][action])
        self.state = state



def run_experiment(epsilon=1, rounds = 500, episodes=500):
    '''Perform an experiment. Make the agent balance the pole'''
    
    env = gym.make('CartPole-v0')

    agent = Agent(env)

    # get environment
    
    env.env.seed(1)     # seed for reproducibility
    obs = env.reset()

    plot = False

    steps_per_round = []

    for episode in range(episodes):
        
        position_list = []
        velocity_list = []
        angle_list = []
        angular_velocity_list = []
        steps = []
        total_rounds = 0

        for round in range(rounds):

            env.render()

            p = np.random.random()

            if p < epsilon: 
                action = agent.choice()
            else:
                action = agent.greedy_action()
           
            # apply action
            obs, reward, done, _ = env.step(action)

            state = agent.discretize(obs)
                        
            agent.get_reward(action,state,reward)

            position_list.append(obs[0])
            velocity_list.append(obs[1])
            angle_list.append(obs[2])
            angular_velocity_list.append(obs[3])
            steps.append(round)
            total_rounds += round            

            if done:
                if round > 150:
                    print(f'Threshold reached after {round+1} iterations.')
                if round < 199:
                    position_list = []
                    velocity_list = []
                    angle_list = []
                    angular_velocity_list = []
                    steps = []
                else:
                    position = position_list
                    velocity = velocity_list
                    angle = angle_list
                    angular_velocity = angular_velocity_list
                    time = steps
                    plot = True
                break           

        epsilon = epsilon - 0.01
        if epsilon < 0.01:
            epsilon = 0.01
        
        env.reset()

        steps_per_round.append(round)
    
    env.close()
    
    if plot:
        fig, ax = plt.subplots(2,2, figsize=(15,8))
        ax[0][0].plot(time, position)
        ax[0][0].set_xlabel('Time steps')
        ax[0][0].set_ylabel('Position (m)')
        ax[0][0].grid()
        
        ax[0][1].plot(time, velocity, 'r')
        ax[0][1].set_xlabel('Time steps')
        ax[0][1].set_ylabel('Velocity (m/s)')
        ax[0][1].grid()
        
        ax[1][0].plot(time, angle, 'g')
        ax[1][0].set_xlabel('Time steps')
        ax[1][0].set_ylabel('Angle (rad)')
        ax[1][0].grid()
        
        ax[1][1].plot(time, angular_velocity, 'y')
        ax[1][1].set_xlabel('Time steps')
        ax[1][1].set_ylabel('Angular Velocity (rad/s)')
        ax[1][1].grid()

        plt.suptitle('Observations per step')
        plt.tight_layout()
        plt.show()

        fig, ax = plt.subplots(1,1, figsize=(15,8))
        ax.plot(np.arange(0,episodes), steps_per_round)
        ax.set_xlabel('Episodes')
        ax.set_ylabel('Iterations')
        plt.suptitle('Total iterations per episode')
        plt.show()

    print("After {} episodes the average cart steps before done was {}".format(episodes,np.mean(steps_per_round)))

if __name__ == '__main__': 
    run_experiment() 