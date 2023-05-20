from models.dfa import DFA
from models.nfa import NFA
from helpers.fa_helper import FiniteAutomataHelper

# this dfa can be minimized
start_state = 'q0'
alphabet = {'a', 'b'}
transition_function = {
    'q0': {'a': 'q6', 'b': 'q1'},
    'q1': {'a': 'q2', 'b': 'q4'},
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

print(automata.minimize_dfa().transitions)

# this is already minimized
transition_function = {
    'p0': {'a': 'p1', 'b': 'p0'},
    'p1': {'a': 'p2', 'b': 'p3'},
    'p2': {'a': 'p4', 'b': 'p5'},
    'p3': {'a': 'p6', 'b': 'p3'},
    'p4': {'a': 'p4', 'b': 'p5'},
    'p5': {'a': 'p7', 'b': 'p7'},
    'p6': {'a': 'p2', 'b': 'p8'},
    'p7': {'a': 'p7', 'b': 'p7'},
    'p8': {'a': 'p9', 'b': 'p7'},
    'p9': {'a': 'p5', 'b': 'p10'},
    'p10': {'a': 'p9', 'b': 'p7'},
}

states = {'p7', 'p5', 'p4', 'p3', 'p8', 'p6', 'p1', 'p9', 'p10', 'p2', 'p0'}

final_states = {'p3', 'p6', 'p8', 'p2', 'p5'}

start_state = 'p0'

alphabet = {'a', 'b'}

dfa = DFA(start_state, final_states, transition_function, alphabet, states)

# m_dfa = dfa.minimize_dfa()


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
print(dfa.minimize_dfa().transitions)
