
class Action:
    def __init__(self):
        pass
    def __repr__(self):
        return self.__class__.__name__
    def to_coq(self):
        return self.coq_str
    def __hash__(self):
        return hash(self.coq_str)
    def __eq__(self, other):
        return hash(self) == hash(other)

class ApplyAntisymmetric(Action):
    def __init__(self):
        self.coq_str = "apply antisymmetric."

class ApplyMeetDefinition(Action):
    def __init__(self):
        self.coq_str = "apply meet_is_inf."

class ApplyJoinDefinition(Action):
    def __init__(self):
        self.coq_str = "apply join_is_sup."

class ApplyMeetIsLowerBound(Action):
    def __init__(self):
        self.coq_str = "apply meet_is_lb."

class ApplyJoinIsUpperBound(Action):
    def __init__(self):
        self.coq_str = "apply join_is_ub."

class Reflexivity(Action):
    def __init__(self):
        self.coq_str = "reflexivity."

class SplitTheAndStatement(Action):
    def __init__(self):
        self.coq_str = "split."

class ApplyTransitivity(Action):
    def __init__(self, y):
        self.coq_str = "apply transitivity with (y := {}).".format(y)

class Undo(Action):
    def __init__(self):
        self.coq_str = "Undo."

all_actions = [ApplyAntisymmetric(), 
ApplyMeetDefinition(), ApplyJoinDefinition(), 
ApplyMeetIsLowerBound(), ApplyJoinIsUpperBound(),
Reflexivity(), SplitTheAndStatement()
, ApplyTransitivity(y="a ⊓ b"), ApplyTransitivity(y="b ⊓ c")
#, ApplyTransitivity(y="a ⊔ b"), ApplyTransitivity(y="b ⊔ c")
#, Undo() # deprecating the Undo action, since it messes up the proof search

]
