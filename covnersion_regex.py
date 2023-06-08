import helpers.reg_exp_helper as regex_converter
from helpers.fa_helper import FiniteAutomataHelper
import helpers.graph_helper as graph_helper


polish_regex = regex_converter.polish_regex(
    '(c)(c)*((d)($))+(((a)((a)(b)+(b))+(d))($)+(((a)((a)(a)))(a)*($)+((a)((a)($)+($)))))')
print(polish_regex)

expression_tree = regex_converter.make_exp_tree(polish_regex)
finite_automata = regex_converter.compute_regex(expression_tree)

regex_converter.arrange_nfa(finite_automata)

nfa = regex_converter.change_nfa_form()
print('--------')
print(nfa.states)
print('--------')
print(nfa.final_states)
print('--------')
print(nfa.start_state)
print('--------')
print(nfa.alphabet)
print('--------')

nfa.enfa_to_nfa()
for item in nfa.transitions.items():
    print(item)

helper = FiniteAutomataHelper()

dfa = helper.nfa_to_dfa(nfa)
print('-----NFA_STATES-----')
print(len(dfa.states))
print(len(dfa.final_states))
print('-----NFA_STATES-----')
print(dfa.start_state)
print(dfa.final_states)
for item in dfa.transitions.items():
    print(item)

dfa = dfa.minimize_dfa()

print(len(dfa.states))
print(len(dfa.final_states))
