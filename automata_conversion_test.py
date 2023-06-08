from models.nfa import NFA
from helpers.fa_helper import FiniteAutomataHelper

transition_function = {
    ('q1', '$'): {'q2', 'q3'},
    ('q2', '0'): {'q4'},
    ('q4', '$'): {'q3', 'q2'},
    ('q3', '$'): {'q5'},
    ('q5', '1'): {'q6'},
    ('q6', '$'): {'q7'},
    ('q7', '$'): {'q8', 'q9'},
    ('q8', '0'): {'q10'},
    ('q10', '$'): {'q8', 'q9'},

}

start_state = 'q1'
states = {'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'}
final_states = {'q9'}
alphabet = {'0', '1'}

nfa = NFA(start_state, final_states, transition_function, alphabet, states)

helper = FiniteAutomataHelper()
nfa.enfa_to_nfa()


dfa = helper.nfa_to_dfa(nfa)

print(dfa.minimize_dfa().transitions)
