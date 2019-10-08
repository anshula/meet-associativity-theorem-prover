import numpy as np
from state import State
from qtable import QTable
from printsettings import PRINT_ACTIONS_TAKEN
from actions import Undo


class Agent:
    def __init__(self):
        self.qtable = QTable()

    def load_definitions(self, *defs):
        pass

    def train(self, env, epsilon=0.1, update_q_table=True):
        # RL training parameters
        alpha=0.1
        gamma=0.6
        
        steps = 0
        while not env.state.done:
            # ------------------------------------
            # Choose to explore or exploit
            # ------------------------------------
            if np.random.uniform(0, 1) < epsilon: # Explore action space
                action = self.qtable.get_random_action(env.state) 
            else: # Exploit the action space
                action = self.qtable.get_recommended_action(env.state) 

            if PRINT_ACTIONS_TAKEN: print(action, "\n\n")

            old_state = env.state.get_copy()
            next_state, reward, done, to_undo = env.step(action) # will return error and undo, if unsuccessful
            # ------------------------------------
            # Update the qtable
            # ------------------------------------
            if update_q_table and not isinstance(action, Undo): 
                self.qtable.update(old_state, next_state, action, reward, alpha, gamma)

            # ------------------------------------
            # if it's an already visited state, you should undo it so the proof search goes faster
            # ------------------------------------
            if to_undo:
                env.step(Undo())


            steps += 1

        print("The proof of", env.theorem.name)
        print("...took", steps, "steps.")
        print("Proof generated:", env.state.past_actions)

    def evaluate(self, env):
        self.train(env, epsilon=0, update_q_table=True) # only exploit, not explore

    def apply_antisymmetry(self):
        pass