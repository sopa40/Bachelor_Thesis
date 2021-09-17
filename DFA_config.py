### DFA parameters: @DFA_config.max_states_number, @DFA_config.max_transition_number, @DFA_config.max_alphabet_number. 
### Alphabet and states are named from 0 to max value
### DFA representation: as dictionary 
### {start_state: {transition_symbol: end_state} }
### {int : {int : int} }
### doubled states are notated as (state_1, state_2), singletons as state_1

### if the format of the DFA does not correspond to the one above, either error or wrong evaluations are possible.

### symbols are needed mainly to concatenate two states and for transitions, short path is not calculated yet

## DFA parameters
max_states_number = 10
max_transition_number = 19
max_alphabet_number = 2
alphabet = list(range(max_alphabet_number))

### parameter for maximum suitable DFA to be tested 
max_count = 10000
