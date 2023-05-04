import dfa

start_state = 'q0'
alphabet = {'0', '1'}
transition_function = {
    'q0': {'0': 'q0', '1': 'q1'},
    'q1': {'0': 'q1', '1': 'q0'}
}
accept_states = {'q0'}
states = {'q0', 'q1'}

print(transition_function)
print(transition_function['q0'])
print(transition_function['q1']['0'])