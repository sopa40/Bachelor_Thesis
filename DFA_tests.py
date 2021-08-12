from DFA_functionality import *

### Experiment 0: How many under random @max_count are synchro
def experiment_0(): 
    generated_automata = 0
    non_synchro_count = 0

    while generated_automata < max_count:
        generated_automata += find_non_synchro()
        non_synchro_count += 1

    print("Ex0. Among {} random DFA (with empty) synchro is {}".format(generated_automata, non_synchro_count))



### Experiment 1: How many unique DFA under @max_count are synchro

### RESULT: number of unique (NON_EMPTY) automata raises very quickly, for example for (states, transitions, alphabet)
### (4 4 1) it's 256, (4 4 2) it's 4096, (4 4 3) it's 20736?, (5 5 1 3125), witn (n n 1) it's n^n
### (20 20 1) it's more than 170k
### Without NON_EMPTY restriction number of unique DFAs raises even more drastic
def experiment_1():    
    ### to avoid infinite loops if @max_count is bigger than unique possible
    failed_count_loop = 0 
    failed_count_total = 0
    max_failed_count = max_count
    added_dfa = 0
    unique_dfa_arr = []
    synchro_unique = 0
    while added_dfa < max_count:
        if failed_count_loop >= max_failed_count:
            print ("in experiment 1 bigger @max_count than unique DFA possible")
            break
        unique_dfa = generate_DFA()
        while check_if_empty(unique_dfa):
            unique_dfa = generate_DFA()
        unique_dfa = reorder_transitions(unique_dfa)
        if unique_dfa in unique_dfa_arr:
            failed_count_total += 1
            failed_count_loop += 1
        else:
            unique_dfa_arr.append(unique_dfa)
            added_dfa += 1
            failed_count_loop = 0

    for dfa in unique_dfa_arr:
        if check_synchro(dfa) == 1:
            synchro_unique += 1
            
    print("Ex1. Among {} unique DFA (without empty) synchro is {}. Meanwhile generated repeating DFA {}".format(added_dfa, synchro_unique, failed_count))


### RESULT of comparing Experiment 0 and Experiment 1: almost no difference if we use unique automata or random
### because with number big enough numbers (let's say starting with 8) chance of collision is less than 1/8^8


### Experiment 2: how many random NON_EMPTY DFAs under @max_count are synchro
def experiment_2():
    tested_dfa = 0
    synchro_random = 0
    empty_generated = 0
    while tested_dfa < max_count:
        random_dfa = generate_DFA()
        while check_if_empty(random_dfa):
            empty_generated += 1
            random_dfa = generate_DFA()
        if check_synchro(random_dfa) == 1:
            synchro_random += 1
            
        tested_dfa += 1
        
    print("Ex2. Among {} random DFA (without empty) synchro is {}. Meanwhile generated empty DFA {}".format(tested_dfa, synchro_random, empty_generated))



### Experiment 3: how many random DFAs (with empty DFA inclusive) under @max_count are synchro
def experiment_3(): 
    tested_dfa = 0
    synchro_random = 0
    while tested_dfa < max_count:
        random_dfa = generate_DFA()
        if check_synchro(random_dfa) == 1:
            synchro_random += 1
            
        tested_dfa += 1
        
    print("Ex3. Among {} random DFA (with empty) synchro is {}".format(tested_dfa, synchro_random))


""" 
    ALERT: 
    Experiment 0 and 3 have identic aim, but different approaches. 
    Looks like values are different. To be tested 
"""

### Experiment 4: how many DFA with empty states under @max_count are synchro 

### Important: if @max_transition_number == @max_states_number * @max_alphabet_number, it will not find empty DFA
### So be sure to pick up number suitable for this test
def experiment_4():

    empty_tested = 0
    synchro_empty = 0
    non_empty_generated = 0
    while empty_tested < max_count:
        empty_dfa = generate_DFA()
        while not check_if_empty(empty_dfa):
            non_empty_generated += 1
            empty_dfa = generate_DFA()
            
        if check_synchro(empty_dfa) == 1:
            print(empty_dfa)
            break
            synchro_empty += 1
        empty_tested += 1
        if empty_tested % 1000 == 0:
            print("already tested number is ", empty_tested)
    print("Ex4. Among {} empty DFA synchro is {}. Meanwhile generated non empty DFA {}".format(empty_tested, synchro_empty, non_empty_generated))


### Experiment 5: find a not fully connected DFA with doubled states, but still synchro 
### assuming it should be connected to some strongly connected component of the DFA
def experiment_5():
    """TODO"""


### Experiment 6: find fully connected DFA,  but non synchro
def experiment_6():
    """TODO"""

### Experiment 7: how many tries to generate fully connected
def experiment_7():
    """TODO"""  


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
    
    
    
    ### parameter for maximum suitable DFA to be tested 
    max_count = 1000000

    experiment_0()
    experiment_1()
    experiment_2()
    experiment_3()
    