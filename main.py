from models.dfa import DFA


start_state = 'q0'
alphabet = {'a', 'b'}
transition_function = {
    'q0': {'a': 'q5', 'b': 'q1'},
    'q1': {'a': 'q2', 'b': 'q0'},
    'q2': {'a': 'q4', 'b': 'q7'},
    'q3': {'a': 'q6', 'b': 'q1'},
    'q4': {'a': 'q2', 'b': 'q7'},
    'q5': {'a': 'q0', 'b': 'q5'},
    'q6': {'a': 'q7', 'b': 'q5'},
    'q7': {'a': 'q7', 'b': 'q7'},
}
final_states = {'q1', 'q2', 'q6'}
states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'}
automata = DFA(start_state, final_states, transition_function, alphabet, states)

# print(automata.accept('aaba'))

print(automata.get_unreachable_state())

transition_function = {
    'q0': {'a': 'q1', 'b': 'q0'},
    'q1': {'a': 'q0', 'b': 'q1'},
    'q2': {'a': 'q0', 'b': 'q1'}
}

final_states = {'q1'}
states = {'q0', 'q1', 'q2'}

new_automata = DFA(start_state, final_states, transition_function, alphabet, states)
print(new_automata.get_unreachable_state())