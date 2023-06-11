from models.dfa import DFA
import json
import helpers.reg_exp_helper as regex_converter
from helpers.fa_helper import FiniteAutomataHelper
import helpers.graph_helper as graph_helper

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
automata.minimize_dfa()

start, final, tf, sts = graph_helper.rename_states(automata.start_state,
                                                   automata.final_states, automata.transitions)
print(start)
print(final)
print(sts)
for item in tf.items():
    print(item)


helper = FiniteAutomataHelper()

automata = helper.handle_start_incoming(automata)
automata = helper.handle_end_outgoing(automata)

hop_table = helper.get_input_symbol(automata)

regex = helper.dfa_to_regex(hop_table, automata.start_state,
                            automata.final_states, automata)


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
print(start)
print(final)
print(sts)
for item in tf1.items():
    print(item)
