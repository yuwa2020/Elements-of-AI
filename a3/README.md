

## Part 1  

Problem Outline: Design a solver for a Tic-Tac-Toe adjacent game. Specific rules as follows:
    - Board can be any size NxM
    - Only valid move is to place an 'x', and move cannot be skipped or passed
    - solve() function must provide a move for a board if it is not solved 
        to begin with    
    - solve() function should place a move if there exists a move
    - if there are only losing moves, solve() should still return a move


Intuition:
    Given that this is an adverserial game with "players" taking turns, the obvious choice to solve this problem is Mini-max with alpha beta pruning,
    Usually the most important part of a mini-max or search program is a good heuristic function, especially in cases like this where it may not be possible or the best use of resources to keep mini-maxing until a root node. With an optimal heuristic, we will know for sure that our algorithm will always play optimally. However I cannot gurantee any optimality of heuristics for this version of tic-tac-toe.

    Thinking about possible heuristics, the good guide for this problem is to severely punish losing moves, and any move that is not losing can be given a shot. In this enviroment, players take turns placing the same character, so every non-losing move that is made automatically makes the increases chance of loss for the opposing player. Thus I came up with a heuristic that seeks to maximize the opposing player's chance of loss. 
    
In general the program is set up like so:
    solve() will check if input is acceptable and not sovled, and iterate through all possible remaining moves on the board. Each move is evaluated and compared to a tracked "best" move and score, with better scores and moves replacing them if they are found. This evaluation is done by is_solved() for immediately losing moves and the alpha_beta minimax function and heuristic otherwise. The best move is then played, only playing a losing move if ther are no other options. 

    notQuiteLosing(): 
        Hueristic works like so:
        - Given the board and the tuple x, y for the move, 
        as we will attempt to place a move such that we are as close 
        to losing as possible without actually losing. 
        - Therefore for both sides of each direction, we will check 'n' 
        spaces to see how many back to back 'x's there are without making us, lose, 
        and the score would be higher for each extra 'x' we were able to tack on without hitting 'n' in a row and losing
            - That idea originally sounded great, but ended up being a major problem 
            later on as the check for "losing" moves in the heuristic was causing the 
            heuristic to always return the losing arguemnt completely mess up the minimax,
             with every position being evaluated as a loss.
                - There was never going to a situation for the heuristic where
                    the heuristic was given a losing move, as the moves would already be parsed 
                    for immediate loss in the main solve() function.
                - This caused hours of headaches and led to debugging in the wrong direction. 
                In a debugging session, we figured out this was the problem and managed to slowly resolve other errors, 
                which was much simpler to attack as they weren't errors in logic but about semantics and confusing variable passing. 

    is_goal():
        - The is_goal() function was the first function I wrote to tackle this problem. 
        We need it to help assert that a passed board isn't already solved in the solved() function,
         and it would be helpful in quickly determining whether to continue with a certain line in case it was already losing. 

        - the is_goal() function works like so:
            - for every character on the board, if the character was an 'x', we will look in 4 directions from the character, 
            left, right, down left diagonal, and down right diagonal for 'n' characters.
            If we were able to find 'n' 'x's in any direciton, then the function would immediately return True for solved. 
            - (We used a found flag that is somewhat confusing but works)

    Solve():
        - The solve function was pretty straightforward, especially with the help of the 
        pre-provided functions like parse_board_to_grid() and return_empty_positions().

        is_goal() function helped to streamline many logic here and later on.
        
        - created is_goal() function first to help assert that the board passed in is not 
        already solve, alerting "board is already solved" if it was.

        - Fundamentally, we initialize best_score and best_move vairbales to 
            -inf and none respecively, and evaluate every single possible position left on 
            the board which happens to be all the positions in return_empty_positions() funciton.
            If any of these positions are immediately losing, we set the score for that position 
            to be -inf, and if not, then we pass it on to our alpha-beta minimax alogirthm to receive an evaulation. 
            We then check if the evalation for a certain move is greater than best_score, and update best_score accordingly. 

        - After runnig through every single empty position on the baord, we should have the move accoring to 
        our heuristic, which we will play and return the board. If we do not have a best_move, then that means 
        that every move is losing, and we will simply place a random move. I do realize that placing a random move 
        from the empty positions is not different from placing say, the first move, since we're going to lose, but I find it more interesting. 

    alpha_beta():
        - Maybe the most important part of the algorithm I implemented minimax with alpha beta to evaluate the board.
         Min and max continuously calls each other until they hit a terminal node or run out of depth, attemping to 
         maximize find the best move for max and min players evaluated using our heuristic. Alpha and Beta keeps 
         track of the best scores max and min can guarentee, and when they find a move too good or too bad such that 
         the other would not allow it's play so the branch is pruned as to not waste resources. 

        - Notice that there is no checking for is_goal in alpha_beta because no immeditately losing move would be 
        passed to the function in the first place by solver(). 

    I did have another idea for a heuristic that I did implement, which is "loneliest_move", which was supoosed to 
    reward moves that took up that were put int the spot with the most space, which theoretically would mean that it 
    would become an obstable for opponent move after it, while at the same time minimizing it's own chances of chosing a 
    move that that would make lose. The further away from ofther x's on the board the better. 

    Intuitively I don't see how this is much worse or better than the other heuristic, but it was ultimately
     scrapped as they are quite opposites of each other and I did not have a good idea of how how combine these 
     heuristics for something better than either one seperately. I was testing with notQuiteLosing and with my bugs 
     my priority was not in figuring out how to incorporate this heuristic.

    Further ways to improve: 
        - There are still known and further options to improve and optimize this problem.
        - In a general sense for mini-max with alpha-beta, iterative deepening with memoization table for past layers 
        would would allow a potentially faster and more accurate traversal of the move tree. In a similar vein, the 
        depth we chose to traverse may be dynamically changed based on the size and shape of the board to allow for better performance. 
        - In particular to this problem, further improvement would need to be made in to the heuristics 
        and combining different heuristics for a more accurate assessment for move scoring. For example, 
        complimentary heuristics that maximize for similar features may multiply or add to the final score or 
        heurisitcs in a different direction may lower the combined scores for a final result that considers multiple facets of the problem. 



## Part 2
(1) a description of how you formulated each problem; 
(2) a brief description of how your program works; 

### Train function
Since this part 2 is focused on building HMM inference using the Viterbi algorithm, I created the example below to formulate the train function. This is the first line of the `bc.train`:

Original setence:
```
The DET Fulton NOUN County NOUN Grand ADJ Jury NOUN said VERB Friday NOUN an DET investigation NOUN of ADP Atlanta's NOUN recent ADJ primary NOUN election NOUN produced VERB `` . no DET evidence NOUN '' . that ADP any DET irregularities NOUN took VERB place NOUN . .   
```

Extracted only text 
```
The Fulton County Grand Jury said Friday an investigation of Atlanta's recent primary election produced `` no evidence '' that any irregularities took place . 
```

Extracted only part of speech:
```
DET NOUN NOUN ADJ NOUN VERB NOUN DET NOUN ADP NOUN ADJ NOUN NOUN VERB . DET NOUN . ADP DET NOUN VERB NOUN .   
```

1. Transition probabilities:
- P_{DET NOUN}=4/24, 
- P_{NOUN NOUN}=2/24, P_{NOUN ADJ}=2/24, P_{NOUN VERB}=3/24, P_{NOUN ADP}=1/24, P_{NOUN .}=2/24,
- P_{ADJ NOUN}=2/24, 
- P_{VERB NOUN}=2/24, P_{VERB .}=1/24,
- P_{ADP NOUN}=1/24, P_{ADP DET}=1/24, 
- P_{. DET}=1/24, P_{. ADP}=1/24, 

2. Emission probabilities:
- P(the|DET)=1/4, P(an|DET)=1/4, P(no|DET)=1/4, P(any|DET)=1/4,
- P(Fulton|NOUN)=1/11, P(County|NOUN)=1/11, P(Jury|NOUN)=1/11, P(Friday|NOUN)=1/11, P(investigation|NOUN)=1, P(primary|NOUN)=1/11, P(election|NOUN)=1/11, P(evidence|NOUN)=1/11, P(Atlanta's|NOUN)=1/11, P(irregularities|NOUN)=1/11, P(place|NOUN)=1/11
- P(Grand|ADJ)=1/2, P(recent|ADJ)=1/2,
- P(said|VERB)=1/3, P(produced|VERB)=1/3, P(took|VERB)=1/3,
- P(of|ADP)=1/2, P(that|ADP)=1/2

- P(``|.)=1, P(''|.)=1, , P(.|.)=1, 

3. Initial state probabilities: 
- P(DET)=4/25, P(NOUN)=11/25, P(ADJ)=2/25, P(VERB)=3/25, P(ADP)=2/25 P(.)=3/25


#### *Additional datatypes
idea from https://medium.com/@pradeepbehara/dictionary-vs-defaultdict-in-python-differences-and-use-cases-a702de32c073


I used ```from collections import defaultdictt``` to store the probabilities, since it can handle the missing keys, so it is more efficient than dictionary.

For example, before the train function, I do not need to set 0 for the missing keys, since it will automatically set 0 for the missing keys.
    
After the first line of the train function, each proabbility is sotred like this

transition_probability = 
```
defaultdict(<function Solver.train.<locals>.<lambda> at 0x107bb6980>, {'det': defaultdict(<class 'int'>, {'noun': 4}), 'noun': defaultdict(<class 'int'>, {'noun': 2, 'adj': 2, 'verb': 3, 'det': 1, 'adp': 1, '.': 2}), 'adj': defaultdict(<class 'int'>, {'noun': 2}), 'verb': defaultdict(<class 'int'>, {'noun': 2, '.': 1}), 'adp': defaultdict(<class 'int'>, {'noun': 1, 'det': 1}), '.': defaultdict(<class 'int'>, {'det': 1, 'adp': 1})})
```
emission_probability= 
```
defaultdict(<function Solver.train.<locals>.<lambda> at 0x107bb6a20>, {'det': defaultdict(<class 'int'>, {'the': 1, 'an': 1, 'no': 1, 'any': 1}), 'noun': defaultdict(<class 'int'>, {'fulton': 1, 'county': 1, 'jury': 1, 'friday': 1, 'investigation': 1, "atlanta's": 1, 'primary': 1, 'election': 1, 'evidence': 1, 'irregularities': 1, 'place': 1}), 'adj': defaultdict(<class 'int'>, {'grand': 1, 'recent': 1}), 'verb': defaultdict(<class 'int'>, {'said': 1, 'produced': 1, 'took': 1}), 'adp': defaultdict(<class 'int'>, {'of': 1, 'that': 1}), '.': defaultdict(<class 'int'>, {'``': 1, "''": 1, '.': 1})})
```
initial_probability=
```
defaultdict(<class 'int'>, {'det': 4, 'noun': 11, 'adj': 2, 'verb': 3, 'adp': 2, '.': 3})
```


Before dividing the numbers, the below probabilities match the ones I calculated manually.

Based on this example, the code is implemented.

### Train function:
same in both simple and HMM. 
- transition_probability = based on the previous part of speech, the probability of the next part of speech
- emission_probability = based on the part of speech, the probability of the word
- initial_probability = the probability of the part of speech in the first word of the sentence

First nested loop
```
for words, parts_of_speech in (data):
            for i, (word, part_of_speech) in enumerate(zip(words, parts_of_speech)):
```

Code explanation:
```
 for every line(data) in the data,
    for every word, part_of_speech in the line
        increase total_words
        increase emission_probability[part_of_speech][word]
        increase initial_probability[part_of_speech]
        if it is not the first word in the sentence
            - increase total_of_transitions
            - increase transition_probability
```

The next three basic loops 
```
for part_of_speech in transition_probability:
...
for part_of_speech in emission_probability:
...
for part_of_speech in transition_probability:
```

calculate the probabilities of the transition, emission, and initial probabilities.
- Transition probability is divide by the total number of transitions
- Emission probability is divide by the initial probability of the part of speech, since it calculates the probability based on the given part of speech
- Initial probability is divide by the total number of words in the sentence since it is the first word of the sentence


### 1. Simple 

#### simplified function


```
for every word in sentence
    - max_probability is set to -999
    - predicted_part_of_speech is set to 'noun'
    - for every part_of_speech in emission_probability
        find the part_of_speech that has the highest emission_probability for the word

    - append the predicted_part_of_speech to list_of_parts_of_speech
```


#### Posterior function
It calculates the log of initial probability * emission probability for all words.

### 2. HMM

### hmm_viterbi function:
It uses slide `241106 probabilistic inference.pdf` based on dynamic programming

$$
v_j(t+1) = e_j(O_{t+1}) \max_{1 \leq i \leq N} \left( v_i(t) p_{ij} \right)
$$
where:
- $v_j(t+1)$ is the probability that system is in state $j$ at time $t+1$ $Q_{t+1}= j$
- $e_j(O_{t+1})$ is the probability of observing $O_{t+1}$ given that system is in state $j$ at time $t+1$
- $1 \leq i \leq N$ is max over all possible states at time $t$
- $v_i(t)$ is the probability that system is in state $i$ at time $t$
- $p_{ij}$ is the probability of transition from state $i$ to state $j$

In my code:
- $v_j(t+1)$ is stored in V[t][part_of_speech]
- $e_j(O_{t+1})$ is stored in tmp_emission_probability (if word is not in emission_probability, then it is set to 1e-10)
- $v_i(t)$ is stored in V[t-1][prior_part_of_speech]
- $p_{ij}$ is stored in self.transition_probability[prior_part_of_speech][part_of_speech]
- max_probability is the max over all possible states at time $t$

It will continue all words to find the best path (combination of part of speech).

#### Posterior function
If it's the first word, it calculates:
- log(initial probability * emission probability)

If it's not the first word, it calculates:
- log(transition probability * emission probability)

Then sum all of the probabilities.


### Results (accuracies) for each technique on the test file we’ve supplied, 

- bc.test.tiny 
```
==> So far scored 3 sentences with 42 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       95.24%               66.67%
            2. HMM:       95.24%               66.67%
----
````
- bc.test
```
==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       92.91%               43.15%
            2. HMM:       94.64%               53.55%
----
```





### (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made. 

Initially I used a normal dictionary to store the probabilities, which containes since part of speech tags are fixed, 

This is the code I made before
```
def __init__(self):
        part_of_speech_tags = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
    
        self.transition_probability = {pos: {pos2: 0 for pos2 in part_of_speech_tags} for pos in part_of_speech_tags}
        self.emission_probability = {pos: {} for pos in part_of_speech_tags}
        self.initial_probability = {pos: 0 for pos in part_of_speech_tags}
```


However, after looking at https://medium.com/@pradeepbehara/dictionary-vs-defaultdict-in-python-differences-and-use-cases-a702de32c073
this that DefaultDict can handle the missing keys, so i used defaultdict to store the probabilities. And it actually the probability is higher than dictionary.
This might because the order of the keys in the dictionary is not the same as the order of the keys in the defaultdict as it create new key if it is not present in the dictionary.
I didn't have time to check this but if I have more time, I can check this to improve the accuracy.

