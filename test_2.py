from helpers.fa_helper import FiniteAutomataHelper
from models.dfa import DFA
import helpers.graph_helper as graph_helper
import helpers.reg_exp_helper as regex_converter

regex = '(a+b+c)dc+aa*bb+cd*cc'

polish_regex = regex_converter.polish_regex(
    regex)
print(polish_regex)
expression_tree = regex_converter.make_exp_tree(polish_regex)
finite_automata = regex_converter.compute_regex(expression_tree)
regex_converter.arrange_nfa(finite_automata)
nfa = regex_converter.change_nfa_form()
nfa.enfa_to_nfa()
helper = FiniteAutomataHelper()
dfa = helper.nfa_to_dfa(nfa)
dfa.minimize_dfa()

start, final, tf1, sts = graph_helper.rename_states(dfa.start_state,
                                                    dfa.final_states, dfa.transitions)

print('-------------------DFA1-------------------')
print(start)
print(final)
print(sts)
for item in tf1.items():
    print(item)


dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)

hop_table = helper.get_input_symbol(dfa)


regex = helper.dfa_to_regex(hop_table, dfa.start_state, dfa.final_states, dfa)
polish_regex = regex_converter.polish_regex(
    regex)
print(polish_regex)
expression_tree = regex_converter.make_exp_tree(polish_regex)
finite_automata = regex_converter.compute_regex(expression_tree)
regex_converter.arrange_nfa(finite_automata)
nfa = regex_converter.change_nfa_form()
nfa.enfa_to_nfa()
# helper = FiniteAutomataHelper()
dfa = helper.nfa_to_dfa(nfa)
dfa.minimize_dfa()

start, final, tf2, sts = graph_helper.rename_states(dfa.start_state,
                                                    dfa.final_states, dfa.transitions)
print('-------------------DFA2-------------------')
print(start)
print(final)
print(sts)
for item in tf2.items():
    print(item)

assert tf1 == tf2
assert dfa.accept('eee')
assert dfa.accept('bcd')
assert dfa.accept('aaaa')
assert dfa.accept('bbbb')
assert not dfa.accept('bbb')
