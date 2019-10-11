
# --------------------------------
# Training agent
# --------------------------------

from agent import Agent
from theorems import meetIsAssociative
from environment import Environment
import numpy as np
import random

np.random.seed(0)

agent = Agent()

print("""
# --------------------------------
# Training...
# --------------------------------
""")

env = Environment(meetIsAssociative)
agent.train(env)

print("""
# --------------------------------
# Evaluating...
# --------------------------------
""")

env = Environment(meetIsAssociative)
agent.evaluate(env)