import time
from progress.bar import IncrementalBar
from progress.spinner import Spinner
from DFA_functionality import *
    

### parameter for maximum suitable DFA to be tested 
max_count = 100

### Experiment 0: How many among random @max_count are synchro
"""
def test_0(): 
    generated_automata = 0
    non_synchro_count = 0
    bar = Spinner("While loops looking for non_synchro  ")
    while generated_automata < max_count:
        bar.next()
        generated_automata += find_non_synchro()
        non_synchro_count += 1
        
    bar.finish()
    print("Ex0. Among {} random DFA (with empty) synchro is {}".format(generated_automata, (max_count - non_synchro_count)))
"""


### Experiment 1: How many NON_EMPTY unique DFA among @max_count are synchro

### RESULT: number of unique (NON_EMPTY) automata raises very quickly, for example for (states, transitions, alphabet)
### (4 4 1) it's 256, (4 4 2) it's 4096, (4 4 3) it's 20736?, (5 5 1 3125), witn (n n 1) it's n^n
### (20 20 1) it's more than 170k
### Without NON_EMPTY restriction number of unique DFAs raises even more drastic
def test_1():    
    ### to avoid infinite loops if @max_count is bigger than unique possible
    failed_count_loop = 0 
    failed_count_total = 0
    max_failed_count = max_count
    added_dfa = 0
    unique_dfa_arr = []
    synchro_unique = 0
    look_bar = IncrementalBar('looking for unique automata ', max = max_count)
    while added_dfa < max_count:
        if failed_count_loop >= max_failed_count:
            print ("in experiment 1 @max_count is bigger than unique DFA possible")
            break
        unique_dfa = generate_non_empty_DFA()
        unique_dfa = reorder_transitions(unique_dfa)
        if unique_dfa in unique_dfa_arr:
            failed_count_total += 1
            failed_count_loop += 1
        else:
            unique_dfa_arr.append(unique_dfa)
            added_dfa += 1
            look_bar.next()
            failed_count_loop = 0
            
    print()
    check_bar = IncrementalBar('checking unique automata', max = max_count)
    for dfa in unique_dfa_arr:
        check_bar.next()
        if check_synchro(dfa) == 1:
            synchro_unique += 1
    
    print()
    print("Test 1. Among {} unique DFA (without empty) synchro is {}".format(added_dfa, synchro_unique))
    print("Meanwhile generated repeating DFA {}".format(failed_count_total))


### RESULT of comparing Experiment 0 and Experiment 1: almost no difference if we use unique automata or random
### because with number big enough numbers (let's say starting with 8) chance of collision is less than 1/8^8


### Experiment 2: how many random NON_EMPTY DFAs among @max_count are synchro
def test_2():
    tested_dfa = 0
    synchro_random = 0
    #bar2 = IncrementalBar("Searching ", max = max_count)
    empty_generated = 0
    while tested_dfa < max_count:
        random_dfa = generate_non_empty_DFA()
        if check_synchro(random_dfa) == 1:
            synchro_random += 1
        #bar2.next()
        tested_dfa += 1
    #print()
    #print("Test 2. Among {} random DFA (without empty) synchro is {}".format(tested_dfa, synchro_random))
    return synchro_random


### Experiment 3: how many random DFAs (with empty DFA inclusive) among @max_count are synchro
def test_3(): 
    tested_dfa = 0
    synchro_random = 0
    #bar3 = IncrementalBar('Searching', max = max_count)
    while tested_dfa < max_count:
        random_dfa = generate_DFA()
        if check_synchro(random_dfa) == 1:
            synchro_random += 1
        
        #bar3.next()
        tested_dfa += 1
    
    #print()
    #print("Test 3. Among {} random DFA (with empty) synchro is {}".format(tested_dfa, synchro_random))
    return synchro_random

""" 
    ALERT: 
    Experiment 0 and 3 have identic aim, but different approaches. 
    Looks like values are different. To be tested   
"""

### Experiment 4: how many DFA with empty states among @max_count are synchro 

### Important: if @max_transition_number == @max_states_number * @max_alphabet_number, empty DFA doesn't exist
### So be sure to pick up number suitable for this test
def test_4():
    empty_tested = 0
    synchro_empty = 0
    non_empty_generated = 0
    #bar4 = IncrementalBar("Searching ", max = max_count)
    while empty_tested < max_count:
        #bar4.next()
        empty_dfa = generate_DFA()
        while not check_if_empty(empty_dfa):
            non_empty_generated += 1
            empty_dfa = generate_DFA()
        if (check_synchro(empty_dfa) == 1):
            synchro_empty += 1
        empty_tested += 1
    #print()
    #print("Test 4. Among {} empty DFA synchro is {}". format(empty_tested, synchro_empty))
    #print("Meanwhile generated non empty DFA {}".format(non_empty_generated))
    return synchro_empty

### Experiment 5: find a not fully connected DFA with doubled states, but still synchro 
### assuming it should be connected to some strongly connected component of the DFA
def test_5():
    """TODO"""


### Experiment 6: find fully connected DFA,  but non synchro
def test_6():
    """TODO"""

### Experiment 7: how many tries to generate fully connected
def test_7():
    """TODO"""  

def take_median(func):
    loops_total = 10
    synchro_found = 0
    for i in range(loops_total):
        synchro_found += func()
    return (synchro_found /(max_count * loops_total)) * 100
if __name__ == "__main__":
    
    start_time = time.time()
    
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
    

    print("Parameters are:")
    print("Max number of suitable tested DFA ", max_count)
    print("max_states_number ", max_states_number)
    print("max_transition_number ", max_transition_number)
    print("max_alphabet_number ", max_alphabet_number)
    print("Let's get the party started")
    print()
    test_4()
    
    """
    while (max_transition_number <= max_states_number * max_alphabet_number):
        print("max_transition_number ", max_transition_number)
        print("synchro percentage among non-empty is {}%".format(take_median(test_2)))
        print("synchro percentage among empty is {}%".format(take_median(test_4)))
        print("synchro percentage among random is {}%".format(take_median(test_3)))
        print()
        max_transition_number += 1
    print()
    """
    print("--- Execution took {} seconds ---".format(time.time() - start_time))