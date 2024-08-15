from MDP import MDP
from tqdm import tqdm
import numpy as np
import json 


class ValueIteration(MDP):

    def __init__(self, gamma=0.95, epsilon=10e-10):
        super().__init__()
        self.gamma = gamma
        self.epsilon = epsilon
        self.policy = {}
        self.V = {}

    def _init_V(self):
        for state in self.states:
            self.V[state] = 0
    
    def _init_P(self):
        for state in self.states:
            self.policy[str(state)] = None

    def initialize(self):
        self.generate_states()
        self.generate_actions()
        self.termination_states()
        self._init_V()
        self._init_P()

    def value_iteration(self):
        self.initialize()
        epoch = 0
        while True:
            print(f"Epoch {epoch + 1} started...")
            epoch += 1
            delta = 0
            for s in tqdm(self.states):
                if s in self.T_states:
                    self.V[s] = self.reward_function(s)
                    continue
                v = self.V[s]
                # print('s', s)
                for a in self.actions[s]:
                    expected_value = self.V[s]
                    # next_states = self.possible_next_states(s, a)
                    for s_prime in self.possible_next_states(s, a):
                        # print('s_prime', s_prime, a)
                        expected_value += self.improved_transition_probability(s, a) * (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                    self.V[s] = max(expected_value, self.V[s])
                delta = max(delta, abs(v - self.V[s]))
            if delta < self.epsilon:
                break

        for s in self.states:
            if s in self.T_states:
                continue
            best_action = None
            best_value = float("-inf")
            for a in self.actions[s]:
                expected_value = self.reward_function(s)
                for s_prime in self.possible_next_states(s, a):
                    p_prob = self.improved_transition_probability(s, a)
                    expected_value += p_prob * (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = a
            self.policy[str(s)] = best_action
        with open('value_iteration/policy.json', 'w') as f:
            json.dump(self.policy, f)


if __name__ == '__main__':
    VI = ValueIteration()
    VI.value_iteration()