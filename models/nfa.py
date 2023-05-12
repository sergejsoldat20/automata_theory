class NFA:
    def __init__(self, start_state, final_states, transitions, alphabet, states):
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions 
        self.alphabet = alphabet
        self.states = states

    # check that nfa accepts word 
    def accept(self, word):
        next_states = set([self.start_state])
        for character in word:
            for state in next_states:
                next_states.add(self.transitions[state][character])
        for state in next_states:
            if state in self.final_states:
                return True
        return False
