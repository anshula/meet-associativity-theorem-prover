
import numpy as np
from actions import all_actions, Undo
from printsettings import PRINT_PAST_ACTIONS, PRINT_POSSIBLE_ACTIONS, PRINT_QTABLE

class QTable:
    def __init__(self):
        self.qtable = {}
        self.action_space = all_actions

    def __repr__(self):
        s = ""
        for key, val in self.qtable.items():
            s+=str(key)
            s+="\t"
            s+=str(val)
        return s

    def no_available_actions(self, state):
        possible_actions = state.get_available_actions()

        if PRINT_PAST_ACTIONS: print(state, "\n\t", "Past actions: ", state.past_actions)
        if PRINT_POSSIBLE_ACTIONS: print("\n\t", "Possible actions:", possible_actions)
        if PRINT_QTABLE: 
            if state in self.qtable: print("\n\t", "Qtable", self.qtable[state])
        
        if possible_actions == []: # if there are no possible actions left, this node is dead.  move up the tree
            #print("========= need to go up in proof tree ======")
            return True
        else:
            return False

    def get_recommended_action(self, state):
        if state in self.qtable:
            if self.no_available_actions(state): 
                return Undo()
            else: 
                best_action = max(state.get_available_actions(), key=self.qtable[state].get)
                return best_action

        return self.get_random_action(state)

    def get_random_action(self, state):
        if self.no_available_actions(state): return Undo()
        return np.random.choice(state.get_available_actions())

    def ensure_state_in_qtable(self, state):
        """ If the state is not already in the qtable, add it in with all 0s for each action """
        if state not in self.qtable:
            self.qtable[state.get_copy()] = {action:0.0 for action in self.action_space}
            
    def update(self, state, next_state, action, reward, alpha, gamma):
        """ Update qtable based on reward from last action"""
        self.ensure_state_in_qtable(state) # to avoid key error
        self.ensure_state_in_qtable(next_state) # to avoid key error
        
        old_value = self.qtable[state][action]

        next_max = max(self.qtable[next_state].values()) #get the maximum qtable reward value in next state
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        
        self.qtable[state][action] = new_value