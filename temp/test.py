from PySimpleAutomata import DFA, automata_IO

dfa_example = automata_IO.dfa_dot_importer('dfa.dot')

DFA.dfa_completion(dfa_example)
new_dfa=DFA.dfa_minimization(dfa_example)

automata_IO.dfa_to_dot(new_dfa, 'output-name', '/')