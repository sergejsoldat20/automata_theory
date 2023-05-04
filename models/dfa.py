class DFA:
    def __init__(self, start_state, final_states, transitions, alphabet, states):
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions 
        self.alphabet = alphabet
        self.states = states

    def accept(self, word):
        current_state = self.start_state
        for charachter in word:
            if charachter not in self.alphabet:
                return False 
            current_state = self.transitions[current_state][charachter]
        # if current_state is in the final_states in the end return true
        return current_state in self.final_states         
            

    def has_next_state(self, state):
        reachable_sates = set()
        transition_states = self.transitions[state]
        for character in self.alphabet:
            if character in transition_states[character]:
                reachable_state = transition_states[character]
                reachable_sates.add(reachable_state)
        return reachable_sates;


    def get_unreachable_state(self):
        # we add start state to reachable states
        reachable_states = set()
        for state in self.states:
           reachable_states.add(self.has_next_state(state))
        return reachable_states;

