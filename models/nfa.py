class NFA:
    def __init__(self, start_state, final_states, transitions, alphabet, states):
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions
        self.alphabet = alphabet
        self.states = states

    # this method returns all states where we can go from given state using epsylon '$'
    def epsylon_closure(self, state):
        closure = {state}
        stack = [state]

        while stack:
            current_state = stack.pop()
            epsylon_transitions = self.transitions.get(
                (current_state, '$'), set())
            for epsylon_state in epsylon_transitions:
                if epsylon_state not in closure:
                    closure.add(epsylon_state)
                    stack.append(epsylon_state)

        return closure

    # return target states for given state and symbol, else return ''
    def find_target_states(self, state, symbol):
        target_states = set()
        target_states = self.transitions.get((state, symbol), set())
        if len(target_states) == 0:
            return ''
        else:
            return target_states

    # this method converts epsylon nfa to nfa
    def enfa_to_nfa(self):
        # if start state has epsylon transition to final state we add it to final_states
        start_state_closure = self.epsylon_closure(self.start_state)
        for state in start_state_closure:
            if state in self.final_states:
                self.final_states.add(self.start_state)
                break

        # we create new transition function
        new_transition_function = dict()

        for state in self.states:
            # for every state we find epsylon closure
            state_closure = self.epsylon_closure(state)
            # we initialize dictionary for new transitions
            for symbol in self.alphabet:
                new_transition_function[(state, symbol)] = set()

            # for every state in closure we find if it has next states for symbols in alphabet
            # if it has next states we will find closure for those states and union them for same symbol
            for eps_state in state_closure:
                next_states = {}
                for symbol in self.alphabet:
                    if self.find_target_states(eps_state, symbol) != '':
                        next_states = self.find_target_states(
                            eps_state, symbol)
                        full_closure = set()
                        for n_state in next_states:
                            closure = self.epsylon_closure(n_state)
                            full_closure |= closure

                        new_transition_function[(
                            state, symbol)].update(full_closure)
        # if some key has empty set as value we delete that row from dictionarys
        self.transitions = {
            key: value for key, value in new_transition_function.items() if len(value) > 0}

        return self
