import numpy as np  
import matplotlib.pyplot as plt 
from statistics import mean
import random 

class Env:
    # defining environment
    def __init__(self,actions,states) -> None:
        self.actions = actions
        self.states = states 
        pass

    def is_terminal(self,state):
        # checks if a state is terminal
        # ??? find a better way to do this 
        if state  in [self.states[0],self.states[-1]]:
            return True
        return False 

    def next_state(self,state,action):
        # defines the transition of the environment for a given action
        # Basically returns the next state for a given action at a given state 
        # this is defined as stochastic 
        # for a given action, robot moves in that direction with a probability of 0.8
        # but due to slippery floor, there can be slippages 
        # this can cause the robot to stay in the same location with the probability of 0.15
        # move in the opposite direction with a probability of 0.05 
        # this means , the action is either 1,-1 or zero
        actions = [action , 0*action , -1*action]
        probabilities = (0.8,0.15,0.05) # these are the probabilities of each possible action 
        actual_action = random.choices(actions, weights=probabilities, k=1)[0] 
        if self.is_terminal(state):
            return state 
        return state+actual_action 

    def reward(self,next_state):
        # for a given state and action , what is the collected reward ?

        if next_state==self.states[-1]: # if the next state is collecting the used can 
            r = 5 
        elif next_state == self.states[0]: # if the next state is charging station 
            r =1 
        else:
            r = 0  # for any other thing 
        return r
    def generate_episode(self,state,action,policy):
        # for a given state , action and policy , generate the full episode 
        episode = [] # [[state,action,0]] # zero reward in the beginning 

        while True:
            if self.is_terminal(state):
                episode.append([state,action,0]) # if already at the terminal state , any action gives zero reward
                break
            next_state = self.next_state(state,action)
            reward = self.reward(next_state)
            episode.append([state,action,reward])
            action = policy[next_state]
            state = next_state

        return episode 

    def reset(self):
        # this functions resets the environment , by choosing a random initial state and random action 
        return np.random.choice(self.states),np.random.choice(self.actions)


class MonteCarlo:
    def __init__(self,gamma,env) -> None:
        self.gamma = gamma 
        self.env = env  # this is the defined environment 
        pass
    
    def initialize(self):
        # initializing policy,action value 
        policy = {state:np.random.choice(self.env.actions) for state in self.env.states} # random policy 
        Q = {state:{action:0 for action in self.env.actions} for state in self.env.states}
        Returns = {state:{action:[] for action in self.env.actions} for state in self.env.states}
        return policy,Q,Returns 
    
    def ES(self,n_episodes):
        # Exploring starts 
        # n_episodes - Number of episodes 

        policy,Q,Returns = self.initialize()
        print("Initial Policy",policy)
        for i in range(n_episodes):
            # reset the environment 
            # Choose state and action randomly such that all pair of probability >0  
            state,action = self.env.reset()
            # print(state,action)
            episode = self.env.generate_episode(state,action,policy) # but this episode can have loops and take forever to stop , and may not stop ever 
            # print("Episode",episode)
            G = 0 
            appearances = [(i[0],i[1]) for i in episode] # store only states and actions 
            episode.reverse() # we need trace steps in the backward direction 
            for i,step in enumerate(episode):
                St,At,Rt_1 = step 
                G = self.gamma*G + Rt_1 

                if (St,At) not in appearances[:-(i+1)]:
                    Returns[St][At].append(G)
                    Q[St][At] = mean(Returns[St][At])
                    policy[St] = max(Q[St], key=Q[St].get, default=None) # getting the action with maximum Q 

            # for St,At,Rt_1 in episode: # loop for each step of the episode. Rt_1 is R_t+1
            #     G = self.gamma*G + Rt_1 
            #     # unless St and At appears in the 
            #     if (St,At) not in  appearances:
            #         Returns[St][At].append(G)
            #         Q[St][At] = mean(Returns[St][At])
            #         policy[St] = max(Q[St], key=Q[St].get, default=None) # getting the action with maximum Q 
            #     appearances.append((St,At))
            #     # # print("Step",(St,At,Rt_1))
            #     # print("Q",Q)
            print("policy",policy)
                
            #     # input()
        return policy,Q,Returns

    def on_policy_mc_control(self,epsilon,n_episodes):
        # epsilon is used for epsilon soft policy 
        policy,Q,Returns = self.initialize()
        for i in range(n_episodes):
            # reset the environment 
            # Choose state and action randomly such that all pair of probability >0  
            state,action = self.env.reset()
            # print(state,action)
            episode = self.env.generate_episode(state,action,policy) # but this episode can have loops and take forever to stop , and may not stop ever 
            print("Episode",episode)
            G = 0 



        return 



def main():
    all_actions = [-1,1]
    all_states = [i for i in range(6)]
    env = Env(all_actions,all_states)
    gamma = 0.9 #0.5
    n_episodes = 100 # number of episodes 
    mc = MonteCarlo(gamma,env)
    policy,Q,Returns= mc.ES(n_episodes)
    print(policy)

if __name__ == "__main__":
    main()

    # {0: 1, 1: -1, 2: 1, 3: -1, 4: 1, 5: 1}
    # {0: 1, 1: -1, 2: -1, 3: -1, 4: 1, 5: -1}
