import numpy as np  
import matplotlib.pyplot as plt 


class Env:
    # defining environment
    def __init__(self,all_actions,all_states) -> None:
        self.all_actions = all_actions
        self.all_states = all_states 
        pass

    def actions(self):
        return self.all_actions
    def states(self):
        return self.all_states

    def is_terminal(self,state):
        # checks if a state is terminal
        # find a better way to do this 
        if state  in [self.all_states[0],self.all_states[-1]]:
            return True
        return False 

    def transition(self,state,action):
        # defines the transition of the environment for a given action
        # Basically returns the next state for a given action 
        if self.is_terminal(state):
            return state 
        return state+action 


    def reset(self):
        # this functions resets the environment , by choosing a random initial state and random action 
        return np.random.choice(self.states()),np.random.choice(self.actions())


class MC:
    def __init__(self,env) -> None:
        print(env.reset())
        
        pass



def main():
    all_actions = [-1,1]
    all_states = [i for i in range(6)]
    env = Env(all_actions,all_states)
    mc = MC(env)
    pass

if __name__ == "__main__":
    main()