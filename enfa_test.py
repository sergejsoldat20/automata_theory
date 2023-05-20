from models.nfa import NFA
from helpers.fa_helper import FiniteAutomataHelper
# Example usage
transition_function = {
    ('q0', 'a'): {'q0'},
    ('q0', '$'): {'q1'},
    ('q1', '$'): {'q0'},
    ('q1', 'b'): {'q4', 'q2'},
    ('q2', 'a'): {'q3', 'q2'},
    ('q3', 'b'): {'q3'},
    ('q3', '$'): {'q1'},
    ('q4', 'a'): {'q1'}

}
final_states = {'q1'}
start_state = 'q0'
states = {'q0', 'q1', 'q2', 'q3', 'q4'}
alphabet = {'a', 'b'}

e_nfa = NFA(start_state, final_states, transition_function, alphabet, states)

nfa = e_nfa.enfa_to_nfa()

for item in nfa.transitions.items():
    print(item)
print("---------------------------")
helper = FiniteAutomataHelper()

dfa = helper.nfa_to_dfa(nfa)
print(dfa.start_state)
print(dfa.final_states)
for item in dfa.transitions.items():
    print(item)
print(dfa.alphabet)
print(dfa.states)
dfa.minimize_dfa()
print("----MINIMIZED----")
print(dfa.start_state)
print(dfa.final_states)
for item in dfa.transitions.items():
    print(item)
print(dfa.alphabet)
print(dfa.states)
print("----REGEX----")
dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)

hop_table = helper.get_input_symbol(dfa)

print(helper.dfa_to_regex(hop_table, dfa.start_state, dfa.final_states, dfa))
