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

    states_order = bfs_dfa(transition_function, start_state)
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


def dfs_dfa(transition_function, current_state, visited_states):
    print(current_state)  # Print the current state
    # Add the current state to the set of visited states
    visited_states.add(current_state)

    # Iterate over the transitions for the current state
    for symbol, next_state in transition_function[current_state].items():
        if next_state not in visited_states:
            # Recursively call DFS for the next state
            dfs_dfa(transition_function, next_state, visited_states)

    return list(visited_states)


def find_state_order(start_state, transition_function):
    state_order = [start_state]  # List to store the order of visited states

    if start_state in transition_function:
        transitions = transition_function[start_state]
        print(transitions)
        for symbol, next_state in transitions.items():
            state_order.extend(find_state_order(
                next_state, transition_function))

    return state_order
