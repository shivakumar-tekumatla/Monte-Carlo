import numpy as np  
import matplotlib.pyplot as plt 


class Env:
    # defining environment
    def __init__(self,actions,states) -> None:
        self.actions = actions
        self.states = states 
        pass

    def is_terminal(self,state):
        # checks if a state is terminal
        # find a better way to do this 
        if state  in [self.states[0],self.states[-1]]:
            return True
        return False 

    def next_state(self,state,action):
        # defines the transition of the environment for a given action
        # Basically returns the next state for a given action 
        if self.is_terminal(state):
            return state 
        return state+action 

    def reward(self,state,action):
        # for a given state and action , what is the collected reward ?
        next_state = self.next_state(state,action)
        if next_state==self.states[-1]: # if the next state is collecting the used can 
            r = 5 
        elif next_state == self.states[0]: # if the next state is charging station 
            r =1 
        else:
            r = 0  # for any other thing 
        return r

    def reset(self):
        # this functions resets the environment , by choosing a random initial state and random action 
        return np.random.choice(self.states),np.random.choice(self.actions)


class MC:
    def __init__(self,env) -> None:
        self.env = env  # this is the defined environment 
        pass



def main():
    all_actions = [-1,1]
    all_states = [i for i in range(6)]
    env = Env(all_actions,all_states)
    mc = MC(env)
    pass

if __name__ == "__main__":
    main()