from models.dfa import DFA
import helpers.graph_helper as graph_helper

start_state = 'q0'
alphabet = {'a', 'b', 'c', 'd'}
transition_function = {
    'q0': {'a': 'q3', 'b': 'q11', 'c': 'q9', 'd': 'q7'},
    # 'q1': {'a': 'q6', 'b': 'q1', 'c': 'q2', 'd': 'q3'},
    'q2': {'a': 'q2', 'b': 'q11', 'c': 'q11', 'd': 'q11'},
    'q3': {'a': 'q6', 'b': 'q0', 'c': 'q11', 'd': 'q11'},
    'q4': {'a': 'q2', 'b': 'q11', 'c': 'q11', 'd': 'q11'},
    'q5': {'a': 'q11', 'b': 'q11', 'c': 'q11', 'd': 'q11'},
    'q6': {'a': 'q4', 'b': 'q5', 'c': 'q11', 'd': 'q11'},
    'q7': {'a': 'q11', 'b': 'q11', 'c': 'q11', 'd': 'q11'},
    'q8': {'a': 'q11', 'b': 'q11', 'c': 'q8', 'd': 'q10'},
    'q9': {'a': 'q11', 'b': 'q11', 'c': 'q8', 'd': 'q10'},
    'q10': {'a': 'q11', 'b': 'q11', 'c': 'q11', 'd': 'q11'},
    'q11': {'a': 'q11', 'b': 'q11', 'c': 'q11', 'd': 'q11'},

}
final_states = {'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q10'}
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5',
          'q6', 'q7', 'q8', 'q9', 'q10', 'q11'}
dfa = DFA(start_state, final_states,
          transition_function, alphabet, states)

dfa.minimize_dfa()

for item in dfa.transitions.items():
    print(item)
