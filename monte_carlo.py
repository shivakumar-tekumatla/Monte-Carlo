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

    def reset(self):
        # this functions resets the environment , by choosing a random initial state and random action 
        return np.random.choice(self.states())#,np.random


class MC(Env):
    def __init__(self) -> None:
        
        pass





def main():
    mc = MC()
    pass

if __name__ == "__main__":
    main()