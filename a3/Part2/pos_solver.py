###################################
# CS B551 Fall 2024, Assignment #3
#
# Your names and user ids:
#



import random
import math
from collections import defaultdict
# idea from https://medium.com/@pradeepbehara/dictionary-vs-defaultdict-in-python-differences-and-use-cases-a702de32c073

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        self.transition_probability = defaultdict(lambda: defaultdict(int))
        self.emission_probability = defaultdict(lambda: defaultdict(int))
        self.initial_probability = defaultdict(int)
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        posterior_probability = 0
        if model == "Simple":
            for word, part_of_speech in zip(sentence, label):
                if part_of_speech in self.transition_probability and self.initial_probability[part_of_speech] > 0:
                    initial_probability= math.log(self.initial_probability[part_of_speech])
                else:
                    initial_probability = -999
                if word in self.emission_probability[part_of_speech] and self.emission_probability[part_of_speech][word] > 0:
                    emission_probability = math.log(self.emission_probability[part_of_speech][word])
                else:
                    emission_probability = -999
                posterior_probability += initial_probability + emission_probability
            return posterior_probability
        elif model == "HMM":
            posterior_probability = 0
            for i, (word, part_of_speech) in enumerate(zip(sentence, label)):
                # if it is the first word in the sentence, calculate the initial probability + emission probability
                if i == 0:
                    if part_of_speech in self.initial_probability and self.initial_probability[part_of_speech] > 0:
                        initial_probability = math.log(self.initial_probability[part_of_speech])
                    else:
                        initial_probability = -999
                    if word in self.emission_probability[part_of_speech] and self.emission_probability[part_of_speech][word] > 0:
                        emission_probability = math.log(self.emission_probability[part_of_speech][word])
                    else:
                        emission_probability = -999
                    posterior_probability += initial_probability + emission_probability
                # if it is not the first word in the sentence, calculate the transition probability + emission probability
                else:
                    if label[i-1] in self.transition_probability and part_of_speech in self.transition_probability[label[i-1]] and self.transition_probability[label[i-1]][part_of_speech] > 0:
                        transition_probability = math.log(self.transition_probability[label[i-1]][part_of_speech])
                    else:
                        transition_probability = -999
                    if word in self.emission_probability[part_of_speech] and self.emission_probability[part_of_speech][word] > 0:
                        emission_probability = math.log(self.emission_probability[part_of_speech][word])
                    else:
                        emission_probability = -999
                    posterior_probability += transition_probability + emission_probability
                
            return posterior_probability
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        total_words = 0
        total_of_transitions = 0
        transition_probability = defaultdict(lambda: defaultdict(int))
        emission_probability = defaultdict(lambda: defaultdict(int))
        initial_probability = defaultdict(int)
        for words, parts_of_speech in (data):
            for i, (word, part_of_speech) in enumerate(zip(words, parts_of_speech)):
                total_words += 1
                emission_probability[part_of_speech][word] += 1
                initial_probability[part_of_speech] += 1
                # if it is not the first word in the sentence
                if i != 0:
                    total_of_transitions += 1
                    transition_probability[parts_of_speech[i-1]][part_of_speech] += 1

        # calculate the probabilities
        for part_of_speech in transition_probability:
            for next_part_of_speech in transition_probability[part_of_speech]:
                self.transition_probability[part_of_speech][next_part_of_speech] = transition_probability[part_of_speech][next_part_of_speech] / total_of_transitions

        for part_of_speech in emission_probability:
            for word in emission_probability[part_of_speech]:
                self.emission_probability[part_of_speech][word] = emission_probability[part_of_speech][word] / initial_probability[part_of_speech]

        for part_of_speech in transition_probability:
            self.initial_probability[part_of_speech] = initial_probability[part_of_speech] / total_words


    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        list_of_parts_of_speech = []

        for word in sentence:
            max_probability = -999
            predicted_part_of_speech = 'noun'
            for part_of_speech in self.emission_probability:
                if word in self.emission_probability[part_of_speech] and self.emission_probability[part_of_speech][word] > max_probability:
                    max_probability = self.emission_probability[part_of_speech][word]
                    predicted_part_of_speech = part_of_speech
                
            list_of_parts_of_speech.append(predicted_part_of_speech)
        return list_of_parts_of_speech
        # return [ "noun" ] * len(sentence)

    def hmm_viterbi(self, sentence):
        V = [{} for _ in range(len(sentence))]
        viterbi_path = {}

        # first word in the sentence
        for part_of_speech in self.initial_probability:
            tmp_emission_probability = 1e-10
            if sentence[0] in self.emission_probability[part_of_speech]:
                tmp_emission_probability = self.emission_probability[part_of_speech][sentence[0]]
            V[0][part_of_speech] = self.initial_probability[part_of_speech] * tmp_emission_probability
            viterbi_path[part_of_speech] = [part_of_speech]

        # for the rest of the words in the sentence
        for t in range(1, len(sentence)):
            newpath = {}

            for part_of_speech in self.initial_probability:
                max_probability = -999
                best_state = None
                for prior_part_of_speech in self.initial_probability:
                    tmp_emission_probability = 1e-10
                    if sentence[t] in self.emission_probability[part_of_speech]:
                        tmp_emission_probability = self.emission_probability[part_of_speech][sentence[t]]
                    emission_probability = tmp_emission_probability
                    probability = V[t-1][prior_part_of_speech] * self.transition_probability[prior_part_of_speech][part_of_speech] * emission_probability
                    if probability > max_probability:
                        max_probability = probability
                        best_state = prior_part_of_speech
                V[t][part_of_speech] = max_probability
                newpath[part_of_speech] = viterbi_path[best_state] + [part_of_speech]


            viterbi_path = newpath

        # last word in the sentence
        max_probability = -999
        best_state = None
        for part_of_speech in self.initial_probability:
            if V[-1][part_of_speech] > max_probability:
                max_probability = V[-1][part_of_speech]
                best_state = part_of_speech
        return viterbi_path[best_state]
        
        return [ "noun" ] * len(sentence)
    



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

