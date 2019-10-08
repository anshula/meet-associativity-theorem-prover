class Theorem:
    def __init__(self, name, statement):
        self.name = name
        self.statement = statement
    def to_coq(self):
        return "Theorem {}: {}. Proof. intros.".format(self.name, self.statement)

meetIsAssociative = Theorem("meetIsAssociative", "forall a b c:A, (a ⊓ b) ⊓ c = a ⊓ (b ⊓ c)")
