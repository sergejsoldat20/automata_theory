import helpers.reg_exp_helper as regex_converter
from helpers.fa_helper import FiniteAutomataHelper
import helpers.graph_helper as graph_helper
from models.dfa import DFA

polish_regex = regex_converter.polish_regex(
    '(a+b+c)cd+(aa+bb)+(bcd)*')
print(polish_regex)

expression_tree = regex_converter.make_exp_tree(polish_regex)
finite_automata = regex_converter.compute_regex(expression_tree)

regex_converter.arrange_nfa(finite_automata)

nfa = regex_converter.change_nfa_form()

nfa.enfa_to_nfa()


helper = FiniteAutomataHelper()
dfa = helper.nfa_to_dfa(nfa)

dfa.minimize_dfa()
# (аа|bb)|(a|b|c)cd|a(bcd)
print(dfa.accept(''))


dfa = helper.handle_start_incoming(dfa)
dfa = helper.handle_end_outgoing(dfa)

hop_table = helper.get_input_symbol(dfa)


print(helper.dfa_to_regex(hop_table, dfa.start_state, dfa.final_states, dfa))
