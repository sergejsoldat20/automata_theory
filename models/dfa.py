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

    # this method finds next states for every character in alphabet
    def get_next_states(self, state):
        next_states = set()
        for character in self.alphabet:
            next_states.add(self.transitions[state][character])
        return next_states

    # this method finds and removes unreachable states
    def remove_unreachable_states(self):
        # we add start state to visited_states
        visited_states = set()
        visited_states.add(self.start_state)
        reachable_states_size = 0
        # we go through states and find reachable states
        while (reachable_states_size < len(visited_states)):
            new_states = set()
            reachable_states_size = len(visited_states)
            for state in visited_states:
                new_states.update(self.get_next_states(state))
            visited_states.update(new_states)
        states_to_remove = self.states - visited_states

        # we now remove unreachable states from set of states and from transition function
        for state in states_to_remove:
            del self.transitions[state]
        self.states = self.states - states_to_remove

    # we generate state pairs where first will be final and second won't be final state
    def generate_state_final_pairs(self):
        valid_pairs = set()
        for state1 in self.states:
            for state2 in self.states:
                if state1 in self.final_states and state2 not in self.final_states:
                    if state1 > state2:
                        valid_pairs.add((state1, state2))
                    else:
                        valid_pairs.add((state2, state1))
        return valid_pairs

    # we generate all posible state pairs with different states
    def generate_state_pairs(self):
        all_pairs = set()
        for state1 in self.states:
            for state2 in self.states:
                if state1 != state2:
                    if state1 > state2:
                        all_pairs.add((state1, state2))
                    else:
                        all_pairs.add((state2, state1))
        return all_pairs

    # this method finds next pairs for some pair of states that will be used for minimization algorithm
    def find_next_state_pair(self, state_pair):
        result_pairs = set()
        for character in self.alphabet:
            state1 = self.transitions[state_pair[0]][character]
            state2 = self.transitions[state_pair[1]][character]

            if state1 > state2:
                result_pairs.add((state1, state2))
            else:
                result_pairs.add((state2, state1))
        return result_pairs

    # this method finds unmarked pairs
    def get_unmarked_pairs(self):
        state_pairs = self.generate_state_pairs() - self.generate_state_final_pairs()
        final_pairs = self.generate_state_final_pairs()

        final_pairs_length = 0

        while (final_pairs_length < len(final_pairs)):
            final_pairs_length = len(final_pairs)
            new_pairs = set()
            for pair in state_pairs:
                next_state_pairs = self.find_next_state_pair(pair)
                for next_pair in next_state_pairs:
                    if next_pair in final_pairs:
                        new_pairs.add(pair)

            state_pairs = state_pairs - new_pairs
            final_pairs.update(new_pairs)

        return state_pairs

    # from unmarked pairs we find classes of equivalence
    def get_equivalent_classes(self, unmarked_pairs):
        print(unmarked_pairs)
        equivalent_classes = list()
        equivalent_classes_changed = False

        for pair in unmarked_pairs:
            if len(equivalent_classes) == 0:
                equivalent_classes.append(pair)
            else:
                for i in range(len(equivalent_classes)):
                    if set(equivalent_classes[i]).intersection(set(pair)):
                        equivalent_classes[i] = tuple(
                            set(equivalent_classes[i] + pair))
                        equivalent_classes_changed = True
                if equivalent_classes_changed:
                    equivalent_classes_changed = False
                else:
                    equivalent_classes.append(pair)
        # we find states that are not part of equivalent classes
        states_not_in_eq_classes = [state for state in self.states if state not in set.union(
            *map(set, equivalent_classes))]
        # return set(equivalent_states)
        return set(states_not_in_eq_classes + equivalent_classes)

    def minimize_dfa(self):
        # first we remove unreachble states
        self.remove_unreachable_states()

        if len(self.get_unmarked_pairs()) == 0:
            return self
        # now we find equivalent classes
        equivalent_classes = self.get_equivalent_classes(
            self.get_unmarked_pairs())

        # print(equivalent_classes)

        # we add keys in new_transition_function
        new_transition_function = {}
        for state in equivalent_classes:
            new_transition_function[''.join(list(state))] = {}

        print(equivalent_classes)

        # we loop through every element in states and equivalent_classes
        # we check where states lead in old transition_function
        # if next  state is inside that element than it is looping to itself, else it is showing to other state
        for element in equivalent_classes:
            for state in self.states:
                # print(state)
                if state == element:
                    for character in self.alphabet:
                        next_state = self.transitions[state][character]
                        new_transition_function[''.join(list(state))][character] = self.find_next_state_eq(
                            next_state, equivalent_classes)

                elif state in element:
                    for character in self.alphabet:
                        next_state = self.transitions[state][character]
                        if next_state in element:
                            new_transition_function[''.join(
                                list(element))][character] = ''.join(list(element))
                        else:
                            new_transition_function[''.join(list(element))][character] = self.find_next_state_eq(
                                next_state, equivalent_classes)
        self.transitions = new_transition_function

        # set new start state and new final states
        self.start_state = self.find_next_state_eq(
            self.start_state, equivalent_classes)
        new_final_states = set()
        for f_state in self.final_states:
            new_final_states.add(self.find_next_state_eq(
                f_state, equivalent_classes))
        self.final_states = new_final_states

        # set states to new states
        new_states = set()
        for eq_class in equivalent_classes:
            new_states.add(''.join(eq_class))
        self.states = new_states
        return self

    # this function returns new state from equivalent_classes for old state
    def find_next_state_eq(self, state, equivalent_classes):
        for element in equivalent_classes:
            if state in element:
                return ''.join(list(element))
