from models.nfa import NFA
from helpers.fa_helper import FiniteAutomataHelper

transition_function = {
    ('q0', 'a'): {'q1', 'q2', 'q4'},
    ('q0', 'b'): {'q0'},
    ('q1', 'b'): {'q4', 'q3', 'q5', 'q2', 'q1'},
    ('q1', 'a'): {'q2', 'q5'},
    ('q2', 'b'): {'q5'},
    ('q2', 'a'): {'q2'},
    ('q3', 'a'): {'q4'},
    ('q4', 'b'): {'q3'},
    ('q4', 'a'): {'q5'},
}

start_state = 'q0'
states = {'q0', 'q1', 'q3', 'q4', 'q5'}
final_states = {'q5'}
alphabet = {'a', 'b'}

nfa = NFA(start_state, final_states, transition_function, alphabet, states)

helper = FiniteAutomataHelper()

# print(tuple(helper.get_next_states({'q2'}, 'a', nfa)))
'''
dfa = helper.nfa_to_dfa(nfa)
print(dfa.start_state)
print(dfa.final_states)
print(dfa.transitions)
print(dfa.alphabet)
print(dfa.states)
'''
dfa = helper.nfa_to_dfa(nfa)

dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)

hop_table = helper.get_input_symbol(dfa)

print(helper.dfa_to_regex(hop_table, dfa.start_state, dfa.final_states, dfa))
