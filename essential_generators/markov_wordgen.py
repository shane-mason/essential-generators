import random
import sys
import itertools as _itertools
import bisect as _bisect

class Random36(random.Random):
    "Show the code included in the Python 3.6 version of the Random class"


    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
        random = self.random
        if cum_weights is None:
            if weights is None:
                _int = int
                total = len(population)
                return [population[_int(random() * total)] for i in range(k)]
            cum_weights = list(_itertools.accumulate(weights))
        elif weights is not None:
            raise TypeError('Cannot specify both weights and cumulative weights')
        if len(cum_weights) != len(population):
            raise ValueError('The number of weights does not match the population')
        bisect = _bisect.bisect
        total = cum_weights[-1]
        return [population[bisect(cum_weights, random() * total)] for i in range(k)]

class MarcovWordGenerator():

    global_bigrams = ['th'] * 35 + ['he'] * 30 + ['in'] * 24 + ['er'] * 20 + ['an'] * 19 + ['re'] * 18 + ['on'] * 17
    global_bigrams += ['at'] * 14 + ['en'] * 14 + ['nd'] * 13 + ['ti'] * 13 + ['es'] * 13 + ['es'] * 12 + ['or'] * 12
    global_bigrams += ['te'] * 12 + ['ed'] * 11 + ['is'] * 11 + ['it'] * 11 + ['al'] * 10 + ['ar'] * 10 + ['st'] * 10


    def __init__(self):
        self.grams = {}
        self.mat = {}


    def __random_weighted_bigram(self):
        return Random36().choice(MarcovWordGenerator.global_bigrams)

    def make_word(self, length, bigram_start):
        word = bigram_start
        current_bigram = bigram_start
        while len(word) < length:
            transition = self.get_weighted_transition(current_bigram)
            if transition != None:
                word += transition
                current_bigram = word[-2:]
            else:
                current_bigram = self.__random_weighted_bigram()
                word += current_bigram
        return word


    def get_weighted_transition(self, bigram):
        if bigram not in self.mat:
            return None
        res = Random36().choices(self.mat[bigram]['transitions'], weights=self.mat[bigram]['weights'])
        if len(res) > 0:
            return res[0]

        return None



    def condition_grams(self):
        bigram_transitions = {}
        for a,b,c in self.grams:
            bigram = "%s%s" % (a,b)
            print( "%s%s->%s %i" % (a,b,c, self.grams[(a,b,c,)]) )
            if bigram not in bigram_transitions:
                bigram_transitions[bigram] = {}
            if c not in bigram_transitions[bigram]:
                bigram_transitions[bigram][c] = 0
            if 'total' not in bigram_transitions[bigram]:
                bigram_transitions[bigram]['total'] = 0

            bigram_transitions[bigram]['total'] += self.grams[(a,b,c,)]
            bigram_transitions[bigram][c]+=self.grams[(a,b,c,)]

        #now, get the percentages for each
        for bigram in bigram_transitions:
            weights = []
            transitions = []
            for trans in bigram_transitions[bigram]:
                if trans != 'total':
                    percent = bigram_transitions[bigram][trans]/bigram_transitions[bigram]['total']
                    bigram_transitions[bigram][trans] = percent

                    weights.append(percent)
                    transitions.append(trans)

            bigram_transitions[bigram]['weights'] = weights
            bigram_transitions[bigram]['transitions'] = transitions

        self.mat = bigram_transitions

        print(bigram_transitions)

    def extract_ngrams(self, text, n):
        self.grams = {}
        gram_buffer = []

        for letter in text:
            letter = letter.lower()

            if len(gram_buffer) >= n:
                as_tuple = tuple(gram_buffer)
                if as_tuple not in self.grams:
                    self.grams[as_tuple] = 0
                self.grams[as_tuple] += 1
                #print(as_tuple)
                gram_buffer = gram_buffer[1:]

            if letter.isalpha() is True:
                gram_buffer.append(letter)
            else:
                gram_buffer.clear()

set = """Mr. Bennet was so odd a mixture of quick parts, sarcastic humour,
reserve, and caprice, that the experience of three-and-twenty years had
been insufficient to make his wife understand his character. _Her_ mind
was less difficult to develop. She was a woman of mean understanding,
little information, and uncertain temper. When she was discontented,
she fancied herself nervous. The business of her life was to get her
daughters married; its solace was visiting and news."""

set2 = "Hello world so that I can follow this now."

set3 = "lop lod lov love lore log lope london bridge is limp"
gen = MarcovWordGenerator()
gen.extract_ngrams(set, 3)
gen.condition_grams()

weights = [.75, .25, .25]
values = ['a','b','c']
print("-----------------------------------")
print(gen.get_weighted_transition("lo"))
print("Done")

print(gen.make_word(10, 'lo'))