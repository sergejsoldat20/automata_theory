from helpers.fa_helper import FiniteAutomataHelper
from models.dfa import DFA

helper = FiniteAutomataHelper()
transition_function = {
    'q0': {'1': 'q3', '0': 'q1'},
    'q1': {'1': 'q3', '0': 'q0'},
    'q2': {'1': 'q4', '0': 'q1'},
    'q3': {'1': 'q5', '0': 'q5'},
    'q4': {'1': 'q3', '0': 'q3'},
    'q5': {'1': 'q5', '0': 'q5'},
}
final_states = {'q3', 'q5'}
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
start_state = 'q0'
alphabet = {'1', '0'}

dfa = DFA(start_state, final_states, transition_function, alphabet, states)
print("--------------------")
print(dfa.minimize_dfa().transitions)


dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)

hop_table = helper.get_input_symbol(dfa)

print(helper.dfa_to_regex(hop_table, dfa.start_state, dfa.final_states, dfa))


# this can be minimized
transition_function = {
    'q0': {'1': 'q1', '0': 'q3'},
    'q1': {'1': 'q5', '0': 'q2'},
    'q2': {'1': 'q5', '0': 'q2'},
    'q3': {'1': 'q4', '0': 'q0'},
    'q4': {'1': 'q5', '0': 'q2'},
    'q5': {'1': 'q5', '0': 'q5'},
}
final_states = {'q1', 'q2', 'q4'}
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
start_state = 'q0'
alphabet = {'1', '0'}

dfa = DFA(start_state, final_states, transition_function, alphabet, states)
# print(dfa.minimize_dfa().transitions)
print("--------------------")
print(dfa.minimize_dfa().transitions)
print(dfa.final_states)
print(start_state)

dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)

hop_table = helper.get_input_symbol(dfa)

for item in hop_table.items():
    print(item)

print(helper.dfa_to_regex(hop_table, dfa.start_state, dfa.final_states, dfa))
