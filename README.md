# Agent versus Controller approach in balancing CartPole system.
---
Project inspired by [Optimal Control with OpenAI Gym](https://towardsdatascience.com/comparing-optimal-control-and-reinforcement-learning-using-the-cart-pole-swing-up-openai-gym-772636bc48f4) and [Using Q-Learning to solve the CartPole balancing problem](https://medium.com/@flomay/using-q-learning-to-solve-the-cartpole-balancing-problem-c0a7f47d3f9d) articles.

In this project two different approaches of the famous cart pole balancing problem are investigated. The first utilizes the classic Control Theory, with a State Feedback Controller while the second one utilizes a Q-learning ε-greedy Reinforcement Learning approach. The main difference of the two approaches is that in Control Theory we assume that the underlying system dynamics are known in advance, while in Reinforcement Learning the agent either learns a model of the system dynamics (model-based reinforcement learning) or tries to solve a task without a model (model-free reinforcement learning).

<img src="https://miro.medium.com/max/4134/1*gTXYlb78tXVKote7hz21cg.png" align="middle" width="3000"/>

The [CartPole-v1](https://gym.openai.com/envs/CartPole-v1/) environment from OpenAI Gym was used for the experiments that took place.

### The State Feedback Controller approach 

<img src="docs/images/controller.png" align="middle" width="3000"/>

### The Q-learning ε-greedy approach

<img src="docs/images/q-learning.png" align="middle" width="3000"/>

<img src="docs/images/iterations-per-episode.png" align="middle" width="3000"/>
