class EpsylonNFA:
    def __init__(self, start_state, final_states, transitions, alphabet, states):
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions 
        self.alphabet = alphabet
        self.states = states