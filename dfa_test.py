from models.dfa import DFA
import json
from helpers.fa_helper import FiniteAutomataHelper

start_state = 'q0'
alphabet = {'a', 'b'}
transition_function = {
    'q0': {'a': 'q6', 'b': 'q1'},
    'q1': {'a': 'q0', 'b': 'q4'},
    'q2': {'a': 'q5', 'b': 'q3'},
    'q3': {'a': 'q8', 'b': 'q3'},
    'q4': {'a': 'q6', 'b': 'q8'},
    'q5': {'a': 'q2', 'b': 'q3'},
    'q6': {'a': 'q4', 'b': 'q7'},
    'q7': {'a': 'q8', 'b': 'q7'},
    'q8': {'a': 'q7', 'b': 'q4'},
    'q9': {'a': 'q10', 'b': 'q8'},
    'q10': {'a': 'q3', 'b': 'q9'},
}
final_states = {'q1', 'q4', 'q8'}
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'}
automata = DFA(start_state, final_states,
               transition_function, alphabet, states)

# print(automata.accept('aaba'))

# print(automata.get_unreachable_state())

# print(len(automata.generate_state_pairs()))

# print(automata.generate_state_pairs() - automata.generate_state_final_pairs())

# print(automata.get_equivalent_states())

# equivalent_pairs = automata.get_equivalent_states()

# print(automata.get_equivalent_classes(equivalent_pairs))
automata_helper = FiniteAutomataHelper()

# print(automata_helper.get_predecessors_successors("q3", automata))
'''
print(automata_helper.check_state_loop("q0", automata))
print(automata_helper.check_state_loop("q7", automata))
print(automata_helper.check_state_loop("q3", automata))

print(automata_helper.start_has_incoming(automata))
print("------------")
'''
start_state = 'q0'
alphabet = {'a', 'b'}
transition_function = {
    'q0': {'a': 'q0', 'b': 'q1'},
    'q1': {'a': 'q1', 'b': 'q2'},
    'q2': {'a': 'q2', 'b': 'q2'},
}
final_states = {'q1', 'q2'}
states = {'q0', 'q1', 'q2'}
automata = DFA(start_state, final_states,
               transition_function, alphabet, states)
print("regex")
automata = automata_helper.handle_start_incoming(automata)
automata = automata_helper.handle_end_outgoing(automata)
print(automata.start_state)
print(automata.final_states)
print(automata.transitions)
print("============================================")
hop_table = automata_helper.get_input_symbol(automata)

# automata = automata_helper.handle_start_incoming(automata)
# automata = automata_helper.handle_end_outgoing(automata)

# hop_table = automata_helper.get_input_symbol(automata)

for items in hop_table.items():
    print(items)

regex = automata_helper.dfa_to_regex(
    hop_table, automata.start_state, automata.final_states, automata)
print(regex)

for state in states:
    print('state-> ')
    print(state)
    print("-------")
    print(automata_helper.get_predecessors_successors(
        state, hop_table, automata)[0])
