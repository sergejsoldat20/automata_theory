from collections import deque


def bfs_dfa(transition_function, start_state):
    visited = set()
    queue = deque([start_state])

    # we add order of states that we visit, also we add start state
    states_order = list()
    states_order.append(start_state)

    while queue:
        current_state = queue.popleft()
        visited.add(current_state)

        for symbol, next_state in transition_function[current_state].items():
            if next_state not in visited:
                queue.append(next_state)
                visited.add(next_state)
                states_order.append(next_state)
    return states_order


def rename_states(start_state, final_states, transition_function):
    # we do bfs and we get order of states

    states_order = find_state_order(
        transition_function, start_state, len(transition_function.keys()))
    # states_order = find_state_order(start_state, transition_function)
    # we create dictionary with states order and new states order
    new_order = {states_order[i]: 'r' +
                 str(i) for i in range(len(states_order))}

    # we change start state
    new_start_state = new_order[start_state]

    # we set new final states
    new_final_states = [new_order[state] for state in final_states]
    new_final_states = set(new_final_states)

    # we set new transition function
    new_transition_function = {state: dict() for state in new_order.values()}
    for state, transition in transition_function.items():
        for symbol, target_state in transition.items():
            new_transition_function[new_order[state]
                                    ][symbol] = new_order[target_state]
    # we create new dfa

    return new_start_state, new_final_states, new_transition_function, set(new_order.values())


def find_state_order(transition_function: dict, start_state, states_len: int):
    alphabet = sorted(list(transition_function[start_state].keys()))
    states_matrix = list()

    states_matrix.append([start_state])

    while True:

        matrix_row = list()
        for state in states_matrix[-1]:
            for symbol in alphabet:
                # print(transition_function[state][symbol])
                if state_not_in_matrix(transition_function[state][symbol], states_matrix):
                    if transition_function[state][symbol] not in matrix_row:
                        matrix_row.append(transition_function[state][symbol])

        states_matrix.append(matrix_row)
        if sum(len(row) for row in states_matrix) == states_len:
            break

    states_order = list()
    for row in states_matrix:
        states_order += row

    return states_order


def state_not_in_matrix(state, matrix):
    for row in matrix:
        if state in row:
            return False

    return True
