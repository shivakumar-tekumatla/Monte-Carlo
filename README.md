# Monte-Carlo
Monte Carlo with exploring start and on-policy first visit for stochastic cleaning-robot MDP problem. This is Example 2.2 of the book “Reinforcement learning and dynamic programming using function approximators” 

## Exploring Starts 

```Initial Policy {0: {-1: 0.0, 1: 1.0}, 1: {-1: 1.0, 1: 0.0}, 2: {-1: 0.0, 1: 1.0}, 3: {-1: 0.0, 1: 1.0}, 4: {-1: 0.0, 1: 1.0}, 5: {-1: 0.0, 1: 1.0}}

  Final Policy  {0: {-1: 1.0, 1: 0.0}, 1: {-1: 0.0, 1: 1.0}, 2: {-1: 0.0, 1: 1.0}, 3: {-1: 0.0, 1: 1.0}, 4: {-1: 0.0, 1: 1.0}, 5: {-1: 1.0, 1: 0.0}}

  State Value   {0: 0.0, 1: 3.094846635346561, 2: 3.6402342115593473, 3: 4.220072304785156, 4: 4.8300228271812085, 5: 0.0```

Don't worry about any policy at the terminal states 

### Result Plots 

<img src="https://github.com/shivakumar-tekumatla/Monte-Carlo/blob/main/Results/ES_action_value.png" width="700">

<img src="https://github.com/shivakumar-tekumatla/Monte-Carlo/blob/main/Results/ES_state_value_star.png" width="700">

<img src="https://github.com/shivakumar-tekumatla/Monte-Carlo/blob/main/Results/ES_state_value.png" width="700">

## On-Policy First Visit MC Control

```Initial Policy {0: {-1: 0.25, 1: 0.75}, 1: {-1: 0.75, 1: 0.25}, 2: {-1: 0.25, 1: 0.75}, 3: {-1: 0.25, 1: 0.75}, 4: {-1: 0.75, 1: 0.25}, 5: {-1: 0.25, 1: 0.75}}```

```Final Policy  {0: {-1: 0.75, 1: 0.25}, 1: {-1: 0.25, 1: 0.75}, 2: {-1: 0.25, 1: 0.75}, 3: {-1: 0.25, 1: 0.75}, 4: {-1: 0.25, 1: 0.75}, 5: {-1: 0.75, 1: 0.25}}```

```State Value   {0: 0.0, 1: 2.0229257103771903, 2: 2.732817107101685, 3: 3.515765815126021, 4: 4.391217437720262, 5: 0.0}```

Don't worry about any policy at the terminal states 

### Result Plots 

<img src="https://github.com/shivakumar-tekumatla/Monte-Carlo/blob/main/Results/OP_MC_action_value.png" width="700">

<img src="https://github.com/shivakumar-tekumatla/Monte-Carlo/blob/main/Results/OP_MC_state_value_star.png" width="700">

<img src="https://github.com/shivakumar-tekumatla/Monte-Carlo/blob/main/Results/OP_MC_state_value.png" width="700">
