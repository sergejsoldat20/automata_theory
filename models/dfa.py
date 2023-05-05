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
            

    def get_next_states(self, state):
        next_states = set()
        for character in self.alphabet:
            next_states.add(self.transitions[state][character])
        return next_states


    def get_unreachable_state(self):
        # we add start state to visible states
        visited_states = set() 
        visited_states.add(self.start_state)
        reachable_states_size = 0
        while(reachable_states_size < len(visited_states)):
            new_states = set()
            reachable_states_size = len(visited_states)
            for state in visited_states:
                new_states.update(self.get_next_states(state))
            visited_states.update(new_states)
        return self.states - visited_states



