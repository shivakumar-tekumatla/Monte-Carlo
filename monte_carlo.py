import numpy as np  
import matplotlib.pyplot as plt 
from statistics import mean
from copy import deepcopy
import random 
random.seed(0)

class Env:
    # defining environment
    def __init__(self,actions,states) -> None:
        self.actions = actions
        self.states = states 
        self.terminal_states = [self.states[0],self.states[-1]]
        pass

    def is_terminal(self,state):
        # checks if a state is terminal
        # ??? find a better way to do this 
        if state  in self.terminal_states:
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
            # next action is selected based on the probability of taking it 
            action = random.choices(list(policy[next_state].keys()), weights=tuple(policy[next_state].values()), k=1)[0] 
            # action = policy[next_state]
            state = next_state

        return episode 

    def reset(self):
        # this function resets the environment , by choosing a random initial state and random action 
        return random.choice(self.states),random.choice(self.actions)


class MonteCarlo:
    def __init__(self,gamma,env) -> None:
        self.gamma = gamma 
        self.env = env  # this is the defined environment 
        pass
    
    def initialize(self,epsilon):
        # generalizing this function for both ES and on-policy control epsilon soft 
        # when epsilon =0 , the initialization is for ES 
        # initializing policy,action value 
        n_actions = len(self.env.actions)
        p = epsilon/n_actions

        # so for one action we have probability of choosing is 1-epsilon+p , and for the rest probability of choosing is p 
        # to initialize a random policy , we can take one action at random, and give it the best probability , adn for the rest probability p 

        probabilities = {action:p for action in self.env.actions}
        probabilities[random.choice(list(probabilities))] = 1-epsilon+p  # this will be randomized when assigned as the actual policy 
        
        policy = {state:{action:0 for action in self.env.actions} for state in self.env.states}
        for state in self.env.states:
            temp = list(probabilities.values())
            random.shuffle(temp)
            policy[state] = dict(zip(probabilities, temp))

        Q = {state:{action:0 for action in self.env.actions} for state in self.env.states}
        Returns = {state:{action:[] for action in self.env.actions} for state in self.env.states}
        return policy,Q,Returns 
    
    def update_policy(self,policy,St,A_star,epsilon):
        # when epsilon is zero , refers to Exploring start 
        n_actions = len(self.env.actions)
        p = epsilon/n_actions
        for action in policy[St]:
            policy[St][action] = p
        policy[St][A_star] = 1-epsilon+p #for the best action, assign more probability 
        return policy 

    def state_value(self,policy,Q):
        V = {state:sum([policy[state][action]*Q[state][action] for action in policy[state]]) for state in self.env.states }
        return V 

    def plot_state_value(self,Vs,title):
        n = len(Vs)

        episodes = [i+1 for i in range(n)]
        ys =[list(V.values()) for V in Vs]
        legend = ["state "+str(key) for key in Vs[0]]
        plt.plot(episodes,ys)
        plt.title(title)
        plt.xscale('log',base=10)
        plt.xlabel("Episodes (log scale)")
        plt.ylabel("State Value for each state")
        plt.legend(legend, loc='lower right')
        plt.show()
    
    def plot_action_value(self,Qs,title):
        # for Q in Qs:
        #     print(Q)
        #     input()
        n = len(Qs)
        episodes = [i+1 for i in range(n)]
        ys =[]
        for Q in Qs:
            y=[]
            for q in Q:
                for s in Q[q]:
                    y.append(Q[q][s])
            ys.append(y)
        # print(ys)
        pairs =[]
        for s in Qs[0]:
            for a in Qs[0][s]:
                pairs.append((s,a))

        legend = [str(pair) for pair in pairs]
        plt.plot(episodes,ys)
        plt.title(title)

        plt.xscale('log',base=10)
        plt.xlabel("Episodes (log scale)")
        plt.ylabel("Action Value for each state")
        plt.legend(legend, loc='lower right')
        plt.show()

            


    def on_policy_mc_control(self,n_episodes,epsilon=0):
        # epsilon is used for epsilon soft policy , and if it is zero , on-policy control is same as Exploring starts 
        policy,Q,Returns = self.initialize(epsilon)
        print("Initial Policy",policy)
        Vs =[]
        V_stars = [] 
        Qs = []
        # policy = 
        for i in range(n_episodes):
            # print("Q",Q)
            # Qs.append(Q.copy())
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
                    A_star = max(Q[St], key=Q[St].get, default=None) # getting the action with maximum Q 
                    policy = self.update_policy(policy,St,A_star,epsilon)
            
            # input("_____")
            Qs.append(deepcopy(Q))
            V_star = {state:max(Q[state].values()) for state in Q}
            V_stars.append(deepcopy(V_star))
            # print(Qs)
            V = self.state_value(policy,Q)
            Vs.append(deepcopy(V))
            # Qs[i] = Q

        # print("Q",Q)
            # print("policy",policy)
            # print("State value ", V)
            # print()
        # V = self.state_value(policy,Q)
        if epsilon ==0:
            add_title = "For Epsilon Start"
        else:
            add_title = "For On-Policy First Visit MC Control"

        self.plot_state_value(V_stars,"Evolution of Optimal State Values over the Episodes "+add_title)
        self.plot_state_value(Vs , "Evolution of the State Values over the Episodes "+add_title)
        self.plot_action_value(Qs,"Evolution of the Action Values over the Episodes "+add_title)
        return policy,Q,Returns,V 



def main():
    all_actions = [-1,1]
    all_states = [i for i in range(6)]
    env = Env(all_actions,all_states)
    gamma = 0.9 #0.5
    n_episodes = 1000 # number of episodes 
    mc = MonteCarlo(gamma,env)
    policy,Q,Returns,V= mc.on_policy_mc_control(n_episodes,epsilon=0) # exploring starts 
    print("Final Policy ",policy)
    print("State Value  ",V)
    policy,Q,Returns,V= mc.on_policy_mc_control(n_episodes,epsilon=0.5) # on-policy control 
    print("Final Policy ",policy)
    print("State Value  ",V)

if __name__ == "__main__":
    main()

    # {0: 1, 1: -1, 2: 1, 3: -1, 4: 1, 5: 1}
    # {0: 1, 1: -1, 2: -1, 3: -1, 4: 1, 5: -1}
