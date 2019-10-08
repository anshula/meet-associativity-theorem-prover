class Poset:
    def to_coq():
        return """
        Require Import Coq.Program.Program.
        Require Import Coq.Relations.Relations.
        Require Import Coq.Classes.RelationClasses.

        Generalizable All Variables.
        
            Class Poset (A : Set) := {
                ord : relation A;

                reflexive :> Reflexive ord;
                antisymmetric : forall {x y}, ord x y -> ord y x -> x = y;
                transitive :> Transitive ord
            }.

            Infix "≤" := ord (at level 50).
            """

class Lattice:
    def to_coq():
        return """
            Reserved Infix "⊓" (at level 40, left associativity).
            Reserved Infix "⊔" (at level 36, left associativity).

            Class Lattice (A : Set) `(Poset A) := {

              (* Meet and join take two elements of the set A and output another*)
              meet : A -> A -> A where "x ⊓ y" := (meet x y);
              join : A -> A -> A where "x ⊔ y" := (join x y);

              (* Meet is equivalent to the infimum*)
              meet_is_inf : forall a b : A,
              forall x, x ≤ a /\ x ≤ b <-> x ≤ a ⊓ b;

              (* Join is equivalent to the supremum*)
              join_is_sup : forall a b : A,
              forall x, a ≤ x /\ b ≤ x <-> a ⊔ b ≤ x;

            }.

            Infix "⊓" := meet (at level 40, left associativity).
            Infix "⊔" := join (at level 36, left associativity).

            """

class LatticeLemmas:
    def to_coq():
        return """
            
            Lemma meet_is_lb : forall a b : A, a ⊓ b ≤ a /\ a ⊓ b ≤ b.
            Proof.
              intros.
              apply meet_is_inf.
              reflexivity.
            Qed.

            Lemma join_is_gb : forall a b : A, a ≤ a ⊔ b  /\ b ≤ a ⊔ b.
            Proof.
              intros.
              apply join_is_sup.
              reflexivity.
            Qed.
            """
