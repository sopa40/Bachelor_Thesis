import random

### TODO:   1. check how many with >=1 empty state are synchro
###         2. exclude empty states
###-------------------------------------------------------------------###


### DFA representation: as dictionary key value
### {start_state: {transition_symbol: end_state} }
### {int : {int : int} }
### doubled states are notated as (state_1, state_2), singletons as state_1

### if the format of the DFA does not correspond to the one above, either error or wrong evaluations are possible.

### symbols are needed mainly to concatenate two states, short path is not calculated yet

### if there are more max_transitions than possible with current max_states and alphabet, the program will fall in
### infinite loop so choose the numbers carefully. Maybe later checking will be added

max_states_number = 20
max_transition_number = 30
max_alphabet_number = 2
alphabet = set(range(max_alphabet_number))

def generate_transitions():
    begin_state = random.randint(0, max_states_number - 1)
    end_state = random.randint(0, max_states_number - 1)
    letter = random.randint(0, max_alphabet_number - 1)
    return begin_state, letter, end_state

def add_transition(dfa, transition):
    start_state = transition[0]
    end_state = transition[2]
    letter = transition[1]

    if letter not in dfa[start_state]:
        dfa[start_state][letter] = end_state
        return 1
    else:
        return 0

### to concatenate all transitions of singletons to a doubled state
def concatenate_two_states(dfa, state_one, state_two):
    new_state = (state_one, state_two)
    dfa[new_state] = dict()

    for (letter, transition) in dfa[state_one].items():
        if letter in dfa[state_two]:
            if transition > dfa[state_two][letter]:
                new_transition = (dfa[state_two][letter], transition)

            elif transition < dfa[state_two][letter]:
                new_transition = (transition, dfa[state_two][letter])

            else:
                new_transition = transition

            dfa[new_state][letter] = new_transition

        else:
            dfa[new_state][letter] = transition

    for (letter, transition) in dfa[state_two].items():
        if letter in dfa[state_one]:
            pass
        else:
            dfa[new_state][letter] = transition

    return dfa

### BFS starting from @start_state with current @dfa transitions untill singleton reached.
### return 0 if not possible
def try_reduction(dfa, start_state):
    visited = []
    queue = []
    reset_len = 0
    visited.append(start_state)
    queue.append(start_state)
    while queue:  ### visiting each node
        m = queue.pop(0)

        ### going through a state with no transitions
        if not len(dfa[m].items()):
            continue
        

        for (letter, destination) in dfa[m].items():
            if destination not in visited:
                reset_len += 1
                
                ### if singleton found --> reduction happens
                if type(destination) == int:
                    return start_state, destination, reset_len
                visited.append(destination)
                queue.append(destination)

    return 0

### assuming states_to_remove is doubled state
### removes all states from @all_states assosiated with @reduction
def remove_states(all_states, reduction):
    states_to_remove = reduction[0]
    reduction_dest = reduction[1]
    
    ### deleting the doubled state
    all_states.remove(states_to_remove)

    ### if reduced to one of two states, it stays in all_states to be (possibly) removed later
    if reduction_dest in states_to_remove:
        states_to_remove = tuple(x for x in states_to_remove if x != reduction_dest)

    ### deleting all states containing first or second state
    temp_states = all_states.copy()
    for remove_state in states_to_remove:
        for state in temp_states:
            if remove_state in state:
                all_states.remove(state)

    return all_states

### BFS on @dfa with @start_state
### Return visited states as array
def find_reachable_states(dfa, start_state):
    visited = []
    queue = []
    visited.append(start_state)
    queue.append(start_state)
    while queue:  ### visiting each node
        m = queue.pop(0)
        
        ### going through a state with no transitions
        if not len(dfa[m].items()):
            continue
       
        for (letter, destination) in dfa[m].items():
            if destination not in visited:
                visited.append(destination)
                queue.append(destination)

    return visited

### check via bfs if every vertex can be reached from any
### strongly connected component

### return 1 on success,
###        -1 on at least one state with no connection,
###        0 on unreached vertices (by any other reason)
def check_connected(dfa):
    for state in dfa:
        visited = []
        queue = []
        visited.append(state)
        queue.append(state)
        while queue:

            m = queue.pop(0)
            if dfa[m] == {}:
                return -1

            for (letter, destination) in dfa[m].items():

                if destination not in visited:
                    visited.append(destination)
                    queue.append(destination)

        if len(visited) < len(dfa.keys()):
            return 0

    return 1

### Singletons are not in states_to_compress

### Finding a path to a random singleton. 
### Assuming one can synchronize one singleton to another. Connected component required
### Later addition: work with not only strongly connected components
### By checking whether array of sychronized-to-states can reach some common state (via BFS)

### Looks like strongly connected graphs are always synchronizing

### Return  0 on no reduction found
###         -1 on reductions happend to different components (applicable to not strongly connected)
###         1 on success            
def check_synchro(dfa):
    dfa_extended = generate_double(dfa)

    states_to_compress = set(dfa_extended.keys())
    temp_states = states_to_compress.copy()
    ### for not strongly connected
    reduced_destinations = dict()
    ### removing all singletons, leaving only doubled (not sure if this should be done)
    for state in temp_states:
        if type(state) == int:
            states_to_compress.remove(state)

    temp_states = set() 
    while len(states_to_compress):
        ### no reduction found (no possible)
        if len(temp_states) == len(states_to_compress):  
            return 0

        temp_states = states_to_compress.copy()
        for state in temp_states:
            ### searching for the reduction from any doubled state
            reduced_to = try_reduction(dfa_extended, state)  
            if reduced_to:
                reduced_destinations[reduced_to[1]] = []
                states_to_compress = remove_states(states_to_compress, reduced_to)
                break
    
    ### for not strongly connected
    for state in reduced_destinations.keys():
        reduced_destinations[state] = find_reachable_states(dfa, state)
    
    ret_val = -1
    for reset_state in reduced_destinations.keys():
        if ret_val == 1:
            break
        ### if all states contain reset_state, it will remain 1 after internal for loop
        ret_val = 1
        for state in reduced_destinations.keys():
            if not reset_state in reduced_destinations[state]:
                ret_val = -1
                break
    
    return ret_val 

### When only strongly connected DFAs should be generated, task is easier, but it's a pretty big restriction
### If not only strongly connected - all reduced singletones should be saved and 
### In the end one should check wheter you can synchronize all singletones (path from-to)
def generate_DFA():
    failed_tries = 0
    transition_number = 0
    dfa = {k: dict() for k in range(0, max_states_number)}
    while transition_number < max_transition_number:
        transition = generate_transitions()
        if not add_transition(dfa, transition):
            failed_tries += 1
        else:
            transition_number += 1
            failed_tries = 0
    return dfa

### generates DFA with all doubled states    
def generate_double(dfa):
    states = list(dfa.keys())
    dfa_double = dfa.copy()
    for state_one in states:
        for state_two in states:
            if state_one == state_two or state_one == {} or state_two == {}:
                continue

            if ((state_one, state_two) in dfa_double or
                    (state_two, state_one) in dfa_double):
                continue

            dfa_double = concatenate_two_states(dfa_double, state_one, state_two)

    return dfa_double

def generate_connected_DFA():
    if_connected = 0
    while if_connected != 1:
        generated_DFA = generate_DFA()
        if_connected = check_connected(generated_DFA)
    
    return generated_DFA

### searches for a non-synchro DFA until finds (watchout infinite loops!)
def find_non_synchro():
    count = 0
    ### to enter while condition
    is_synchro = 1
    while is_synchro == 1:
        count += 1            
        if (count % 100 == 0):
            print("count is {}", format(count))
        # dfa = generate_connected_DFA() to work with connected ones
        dfa = generate_DFA()
        is_synchro = check_synchro(dfa)

    print("not sychro, passed tries ", count)
    print(dfa)

if __name__ == "__main__":
    
    ### checking the algorithm with 100% synchronizable automaton. 1 is expected
    # dfa_synchro = {0: {1: 1, 0: 1}, 1: {0: 2, 1: 1}, 2: {0: 3, 1: 2}, 3: {0: 0, 1: 3}}
    # print("IT MUST BE 1! Result", check_synchro(dfa_synchro))

    if max_transition_number < max_states_number:
        print("Unable to generate strongly connected component")
        print("Please increase @max_transition_number to be at least @max_states_number")
        exit()

    if max_transition_number > max_states_number * max_alphabet_number:
        print("too many transitions, infinite loop while generating automaton")
        exit()
    
    find_non_synchro()



# Just an example of printing style: print ("{} holding {}.".format(i,x)) 