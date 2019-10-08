from copy import deepcopy
from actions import all_actions

class State:
    def __init__(self):
        self.past_actions = []

        self.current_subgoal = ""
        self.all_subgoals = tuple()
        self.visited_subgoals = []
        self.num_subgoals = 1

        self.done = False

        self.possible_actions_given_past_actions= {}

    def __str__(self):
        return self.current_subgoal

    def add_attempted_action(self, action):

        past_actions = tuple(self.past_actions)
        if past_actions not in self.possible_actions_given_past_actions:
            self.possible_actions_given_past_actions[past_actions] = all_actions.copy()
        self.possible_actions_given_past_actions[past_actions].remove(action)

    def get_available_actions(self):
        past_actions = tuple(self.past_actions)
        if len(past_actions) > 25: # max out at more than 25 steps
            return []
        if self.num_subgoals > 4: # max out at more than 4 subgoals
            return []
        if past_actions not in self.possible_actions_given_past_actions:
            self.possible_actions_given_past_actions[past_actions] = all_actions.copy()
        return self.possible_actions_given_past_actions[past_actions]

    def append_action(self, action):
        """ Adds last action """
        self.past_actions.append(action)

    def remove_last_action(self):
        """ Removes last action """
        self.past_actions.pop()

    def get_copy(self):
        """ 
        Need a copy for indexing in python dictionary
        Otherwise the state changes, and the key in the dictionary changes with it, and so it is in the wrong hashbucket
        """
        return deepcopy(self)
    
    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """ 
        Hash uses only current_subgoal information (disregards variables, assumptions, and past actions) for qtable 
        """
        # only use last 5 steps...because that's probably the most relevant
        # for what to do next
        return hash(self.current_subgoal)


