from models.ast_node import ExpressionTree, charType, NFAState
from models.nfa import NFA


non_symbols = ['+', '*', '.', '(', ')']
nfa = {}


def make_exp_tree(regexp):
    stack = []
    for c in regexp:
        if c == "+":
            z = ExpressionTree(charType.UNION)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == ".":
            z = ExpressionTree(charType.CONCAT)
            z.right = stack.pop()
            z.left = stack.pop()
            stack.append(z)
        elif c == "*":
            z = ExpressionTree(charType.KLEENE)
            z.left = stack.pop()
            stack.append(z)
        elif c == "(" or c == ")":
            continue
        else:
            stack.append(ExpressionTree(charType.SYMBOL, c))
    return stack[0]


def compPrecedence(a, b):
    p = ["+", ".", "*"]
    return p.index(a) > p.index(b)


def compute_regex(exp_t):
    # returns E-NFA
    if exp_t.charType == charType.CONCAT:
        return do_concat(exp_t)
    elif exp_t.charType == charType.UNION:
        return do_union(exp_t)
    elif exp_t.charType == charType.KLEENE:
        return do_kleene_star(exp_t)
    else:
        return eval_symbol(exp_t)


def eval_symbol(exp_t):
    start = NFAState()
    end = NFAState()

    start.next_state[exp_t.value] = [end]
    return start, end


def do_concat(exp_t):
    left_nfa = compute_regex(exp_t.left)
    right_nfa = compute_regex(exp_t.right)

    left_nfa[1].next_state['$'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]


def do_union(exp_t):
    start = NFAState()
    end = NFAState()

    first_nfa = compute_regex(exp_t.left)
    second_nfa = compute_regex(exp_t.right)

    start.next_state['$'] = [first_nfa[0], second_nfa[0]]
    first_nfa[1].next_state['$'] = [end]
    second_nfa[1].next_state['$'] = [end]

    return start, end


def do_kleene_star(exp_t):
    start = NFAState()
    end = NFAState()

    starred_nfa = compute_regex(exp_t.left)

    start.next_state['$'] = [starred_nfa[0], end]
    starred_nfa[1].next_state['$'] = [starred_nfa[0], end]

    return start, end


def arrange_transitions(state, states_done, symbol_table):
    global nfa

    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        if symbol not in nfa['letters']:
            nfa['letters'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "q" + str(symbol_table[ns])
                nfa['states'].append(q_state)
            nfa['transition_function'].append(
                ["q" + str(symbol_table[state]), symbol, "q" + str(symbol_table[ns])])

        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table)


def notation_to_num(str):
    return int(str[1:])


# def final_st_dfs(st):
#     global nfa
#     for val in nfa['transition_function']:
#         if val[0] == st and val[1] == "$" and val[2] not in nfa["final_states"]:
#             nfa["final_states"].append(val[2])
#             final_st_dfs(val[2])

def final_st_dfs():
    global nfa
    for st in nfa["states"]:
        count = 0
        for val in nfa['transition_function']:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in nfa["final_states"]:
            nfa["final_states"].append(st)


def arrange_nfa(fa):
    global nfa
    nfa['states'] = []
    nfa['letters'] = []
    nfa['transition_function'] = []
    nfa['start_states'] = []
    nfa['final_states'] = []
    q_1 = "q" + str(1)
    nfa['states'].append(q_1)
    arrange_transitions(fa[0], [], {fa[0]: 1})

    st_num = [notation_to_num(i) for i in nfa['states']]

    nfa["start_states"].append("q1")
    # nfa["final_states"].append("Q" + str(sorted(st_num)[-1]))
    # final_st_dfs(nfa["final_states"][0])
    final_st_dfs()
    return nfa


def add_concat(regex):
    global non_symbols
    l = len(regex)
    res = []
    for i in range(l - 1):
        res.append(regex[i])
        if regex[i] not in non_symbols:
            if regex[i + 1] not in non_symbols or regex[i + 1] == '(':
                res += '.'
        if regex[i] == ')' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] == '(':
            res += '.'
        if regex[i] == '*' and regex[i + 1] not in non_symbols:
            res += '.'
        if regex[i] == ')' and regex[i + 1] not in non_symbols:
            res += '.'

    res += regex[l - 1]
    return res


def compute_postfix(regexp):
    stk = []
    res = ""

    for c in regexp:
        if c not in non_symbols or c == "*":
            res += c
        elif c == ")":
            while len(stk) > 0 and stk[-1] != "(":
                res += stk.pop()
            stk.pop()
        elif c == "(":
            stk.append(c)
        elif len(stk) == 0 or stk[-1] == "(" or compPrecedence(c, stk[-1]):
            stk.append(c)
        else:
            while len(stk) > 0 and stk[-1] != "(" and not compPrecedence(c, stk[-1]):
                res += stk.pop()
            stk.append(c)

    while len(stk) > 0:
        res += stk.pop()

    return res


def polish_regex(regex):
    reg = add_concat(regex)
    regg = compute_postfix(reg)
    return regg


def change_nfa_form():
    global nfa
    start_state = nfa['start_states'][0]
    final_states = set(nfa['final_states'])
    alphabet = set(nfa['letters'])

    states = set(nfa['states'])
    transition_function = {}
    # we have to initialize new transition function

    for state in states:
        for char in alphabet:
            transition_function[(state, char)] = set()

    for transition in nfa['transition_function']:
        transition_function[(transition[0], transition[1])].add(transition[2])

    # throw out empty sets
    new_transition_function = {
        key: value for key, value in transition_function.items() if len(value) > 0}

    # we delete $ from alphabet
    alphabet.discard('$')

    return NFA(start_state, final_states, new_transition_function, alphabet, states)
