from models.dfa import DFA
from models.nfa import NFA


class FiniteAutomataHelper:

    def get_input_symbol(self, automata: DFA):
        # we initialize table of hops and fill it with empty strings
        hop_table = {
            state1: {state2: '' for state2 in sorted(list(automata.states))} for state1 in sorted(list(automata.states))
        }

        # we go through transition function and set hop_table[state1][state2] to character
        # state1 has transition to state2
        for state, transition in automata.transitions.items():
            for character, next_state in transition.items():
                if hop_table[state][next_state] == '':
                    hop_table[state][next_state] = character
                else:
                    hop_table[state][next_state] += '+' + character
        return hop_table

    def get_predecessors_successors(self, state, hop_table, automata: DFA):
        predecessors = []
        successors = []
        curr_dict_for_from = {st: {to: v for to, v in val.items(
        ) if to == state} for st, val in hop_table.items()}

        for predecessor in automata.states:
            if predecessor not in curr_dict_for_from.keys() or predecessor == state:
                continue
            if curr_dict_for_from[predecessor][state] != '':
                predecessors.append(predecessor)

        for successor in automata.states:
            if successor not in hop_table[state].keys() or state == successor:
                continue
            if hop_table[state][successor] != '':
                successors.append(successor)
        return predecessors, successors

    def check_state_loop(self, state, automata: DFA):
        next_states = automata.transitions[state].values()
        if state in next_states:
            return True
        return False

    def start_has_incoming(self, automata: DFA):
        check = False
        initial_state = automata.start_state
        for state, transition in automata.transitions.items():
            if initial_state in transition.values():
                check = True
                break
        return check

    def end_has_outgoing(self, automata: DFA):
        # if there is multiple final states return true
        if len(automata.final_states) > 1:
            return True
        # else find that one final state
        final_state = list(automata.final_states)[0]
        # check that there is some state that final has transition to
        if final_state in automata.transitions.keys():
            return True
        return False

    def handle_start_incoming(self, automata: DFA):
        if self.start_has_incoming(automata):
            automata.states.add('qi')
            automata.transitions['qi'] = {'$': automata.start_state}
            automata.start_state = 'qi'

        return automata

    def handle_end_outgoing(self, automata: DFA):
        if self.end_has_outgoing(automata):
            automata.states.add('qf')
            for final_state in automata.final_states:
                automata.transitions[final_state]['$'] = 'qf'
            automata.final_states = 'qf'
        else:
            automata.final_states = list(automata.final_states)[0]
        return automata

    def dfa_to_regex(self, hop_table, state_initial, state_final, automata: DFA):
        for state in sorted(list(automata.states)):
            if state == state_initial or state == state_final:
                continue

            predecessors, successors = self.get_predecessors_successors(
                state, hop_table, automata)

            for predecessor in predecessors:
                if predecessor in hop_table.keys():
                    for successor in successors:
                        if successor in hop_table[predecessor].keys():

                            pre_suc_input_exp = ''
                            self_loop_input_exp = ''
                            from_pre_input_exp = ''
                            to_suc_input_exp = ''

                            if hop_table[predecessor][successor] != '':
                                pre_suc_input_exp = '(' + \
                                    hop_table[predecessor][successor] + ')'

                            if self.check_state_loop(state, automata):
                                self_loop_input_exp = '(' + \
                                    hop_table[state][state] + ')' + '*'

                            if hop_table[predecessor][state] != '':
                                from_pre_input_exp = '(' + \
                                    hop_table[predecessor][state] + ')'

                            if hop_table[state][successor] != '':
                                to_suc_input_exp = '(' + \
                                    hop_table[state][successor] + ')'

                            new_pre_suc_input_exp = from_pre_input_exp + \
                                self_loop_input_exp + to_suc_input_exp

                            if pre_suc_input_exp != '':
                                new_pre_suc_input_exp += ('+' +
                                                          pre_suc_input_exp)

                            hop_table[predecessor][successor] = new_pre_suc_input_exp

            hop_table = {st: {to: v for to, v in inp.items() if to != state}
                         for st, inp in hop_table.items() if st != state}
        return hop_table[state_initial][state_final]

    # this method converts nfa to dfa
    def nfa_to_dfa(self, nfa: NFA):
       #  start_state = {nfa.start_state}
        dfa_states = set()
        dfa_states.add((nfa.start_state, ))
        loop_states = set()
        loop_states.add((nfa.start_state, ))

        transition_matrix = list()
        # print(loop_states)
        # result_states = set()
        states_len = 0
        while (states_len < len(dfa_states)):
            states_len = len(dfa_states)
            dfa_states.update(loop_states)
            for state_set in loop_states:
                for character in nfa.alphabet:
                    next_states = self.get_next_states(
                        state_set, character, nfa)
                    if tuple(next_states) not in dfa_states:
                        dfa_states.add(tuple(next_states))
                    # print(next_states)
            loop_states = dfa_states - loop_states

        dfa_transition_function = dict()

        for item in dfa_states:
            dfa_transition_function[self.join_tuple_elements(item)] = dict()

        for states_tuple in dfa_states:
            for character in nfa.alphabet:
                dfa_transition_function[self.join_tuple_elements(
                    states_tuple)][character] = self.join_tuple_elements(self.get_next_states(states_tuple, character, nfa))

        for item in dfa_transition_function.items():
            print(item)
        print("----------------------")
        # we set new states for dfa, if we have given states like q0q1q2 they will be changed with p0
        # we use dictionary that is mapping old states combination with new states
        states_mapping = dict()
        states_counter = 0
        for state_tuple in dfa_states:
            states_mapping[self.join_tuple_elements(
                state_tuple)] = 'p' + str(states_counter)
            states_counter = states_counter + 1

        # now we change old transition function with new transition function with new states
        new_dfa_transition = dict()

        for state, transition in dfa_transition_function.items():
            new_state = states_mapping[state]
            new_transitions = {}
            for symbol, target_state in transition.items():
                new_target_state = states_mapping[target_state]
                new_transitions[symbol] = new_target_state
            new_dfa_transition[new_state] = new_transitions

        # now we set new states, start_state and final_states
        new_final_states = set()

        # print("-----------")
        for final_state in nfa.final_states:
            for state_tuple in dfa_states:
                if final_state in state_tuple:
                    # print(state_tuple)
                    new_final_states.add(
                        states_mapping[self.join_tuple_elements(state_tuple)])

        new_start_state = ''

        for state_tuple in dfa_states:
            if nfa.start_state in state_tuple and len(state_tuple) == 1:
                new_start_state = states_mapping[self.join_tuple_elements(
                    state_tuple)]
                # print(state_tuple)
                # print("-------------------")
                # print(new_start_state)

        new_states = set(states_mapping.values())
        # print("new states")
        # print(new_states)

        dfa = DFA(new_start_state, new_final_states,
                  new_dfa_transition, nfa.alphabet, new_states)
        return dfa

    def get_next_states(self, states, character, nfa: NFA):
        next_states = set()
        for state in states:
            next_states |= nfa.transitions.get((state, character), set())
        return tuple(sorted(next_states))

    def join_tuple_elements(self, states_tuple: tuple):
        return ''.join(states_tuple)
