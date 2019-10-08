from state import State
from coqinterface import CoqInterface
from definitions import Poset, Lattice, LatticeLemmas
from actions import Undo
import re

class Environment:
    def __init__(self, theorem):
        self.coqinterface = None
        self.theorem = theorem

        self.reset()

    def reset(self):
        if self.coqinterface:
            self.coqinterface.exit()
        
        self.state = State()
        self.coqinterface = CoqInterface(env=self)

        self.load_definitions(Poset, Lattice)
        self.start_section()
        self.load_definitions(LatticeLemmas)
        self.start_theorem()

        self.num_subgoals = 1

    def load_definitions(self, *defs):
        # send definitions of posets and lattice to the environment
        for definition in defs:
            self.coqinterface.sendone(definition.to_coq())

    def start_section(self):
        self.coqinterface.sendone("Section Lattice.  Context `{L : Lattice A}.")

    def start_theorem(self):
        response = self.coqinterface.sendone(self.theorem.to_coq())
        self.update_subgoals(response)

    def update_subgoals(self, response):
        all_subgoals = []
        if "============================" in response:
            num_subgoals = int(response.split(" subgoal")[0].split("\r\n")[-1].strip())        
            self.state.current_subgoal = response.split("============================")[-1].split("\r\n")[1].strip()

            all_subgoals.append(self.state.current_subgoal)

            # get more than first
            if num_subgoals > 1:
                for i in range(2, num_subgoals+1):
                    subgoal = response.split("subgoal {} is:".format(i))[-1].split("\r\n")[1].strip()
                    all_subgoals.append(subgoal)

            # then update the state with that new subgoal
            self.state.all_subgoals = all_subgoals = tuple(sorted(all_subgoals))
            self.state.num_subgoals = num_subgoals

            


    def step(self, action):

        reward = 0
        to_undo = False

        # dont let it undo if the list of last actions is empty.
        if self.state.past_actions == [] and isinstance(action, Undo):
            raise Exception("Tried to undo the first action...so this proof is be impossible to prove given the actions provided.")

        # send to coq
        response = self.coqinterface.sendone(action.to_coq())
        
        # add to list of attempted actions (say that given the subgoal, we tried this action)
        if not isinstance(action, Undo): self.state.add_attempted_action(action)

        # update subgoal according to response
        old_num_subgoals = self.state.num_subgoals
        self.update_subgoals(response)
            
        # if it was undo, we're done -- don't need to do any determining of rewards
        if isinstance(action, Undo): 
            self.state.visited_subgoals.pop() # get rid of the last thing in chain, since we only want visited subgoals in the current path
            return self.state, 0, self.state.done, to_undo

        # if the action worked without error
        if "Error" not in response: 
            reward = -10 # slight negative reward for taking a step
            # append to list of actions
            self.state = self.state.get_copy()
            self.state.append_action(action)

            # try typing qed
            self.coqinterface.sendone("Qed.")
            # make reward even bigger if it was the last step to proving the theorem
            if self.state.done: 
                reward += 100

             
            else:
                # make reward bigger if number of subgoals was reduced.
                # make reward negative if number of subgoals increases
                if  self.state.num_subgoals < old_num_subgoals:
                    reward += 10
                elif  self.state.num_subgoals > old_num_subgoals:
                    reward -= 10

                # if it's an already visited state, you can just undo it
                if self.state.all_subgoals in self.state.visited_subgoals:
                    to_undo = True
                # add in this visited subgoal (so it will be popped in env.step)
                self.state.visited_subgoals.append(self.state.all_subgoals )

        else:
            reward = -1000 # big negative reward for error

        return self.state, reward, self.state.done, to_undo
