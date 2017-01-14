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
    startword = "%"
    stopword = "%"

    def __init__(self):
        self.grams = {}
        self.chain = {}


    def make_word(self, max_len=15, bigram_start="%"):
        word = bigram_start
        current_bigram = bigram_start
        while len(word) < max_len:
            transition = self._get_weighted_transition(current_bigram)
            if transition != None:
                word += transition
                current_bigram = word[-2:]
            else:
                break

        return word.replace(MarcovWordGenerator.startword, "").replace(MarcovWordGenerator.stopword, "")


    def _get_weighted_transition(self, bigram):
        if bigram not in self.chain:
            return None
        res = Random36().choices(self.chain[bigram]['transitions'], weights=self.chain[bigram]['weights'])
        if len(res) > 0:
            return res[0]

        return None


    def _condition_grams(self):
        bigram_transitions = {}
        for a,b,c in self.grams:

            if a == MarcovWordGenerator.startword:
                #not really a bigram in this case
                bigram = "%s" % (a)
                trans_to = "%s%s" % (b,c)

            else:
                bigram = "%s%s" % (a, b)
                trans_to = "%s" % (c)

            #print( "%s%s->%s %i" % (a,b,c, self.grams[(a,b,c,)]) )

            if bigram not in bigram_transitions:
                bigram_transitions[bigram] = {}
            if c not in bigram_transitions[bigram]:
                bigram_transitions[bigram][trans_to] = 0
            if 'total' not in bigram_transitions[bigram]:
                bigram_transitions[bigram]['total'] = 0

            bigram_transitions[bigram]['total'] += self.grams[(a,b,c,)]
            bigram_transitions[bigram][trans_to]+=self.grams[(a,b,c,)]

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

        self.chain = bigram_transitions

        #print(bigram_transitions['+'])

    def _train_on_text(self, text):
        n = 3
        self.grams = {}
        gram_buffer = []

        for letter in text:
            #letter = letter.lower()

            if letter not in ['\n', ' ']:
                gram_buffer.append(letter)
            else:
                gram_buffer.append(MarcovWordGenerator.stopword)

            if len(gram_buffer) >= n:
                as_tuple = tuple(gram_buffer)
                if as_tuple not in self.grams:
                    self.grams[as_tuple] = 0
                self.grams[as_tuple] += 1
                #print(as_tuple)

                gram_buffer = gram_buffer[1:]

            if letter in ['\n', ' ', '*']:
                gram_buffer.clear()
                gram_buffer.append(MarcovWordGenerator.startword)


    def train(self, text):
        self._train_on_text(text)
        self._condition_grams()

    def saveModel(self, filepath):
        import json
        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(self.chain, fp, ensure_ascii=False)

    def loadModel(self, filepath):
        import json
        with open(filepath, 'r') as fp:
            self.chain = json.load(fp)



set1 = """Mr. Bennet was so odd a mixture of quick parts, sarcastic humour,
reserve, and caprice, that the experience of three-and-twenty years had
been insufficient to make his wife understand his character. _Her_ mind
was less difficult to develop. She was a woman of mean understanding,
little information, and uncertain temper. When she was discontented,
she fancied herself nervous. The business of her life was to get her
daughters married; its solace was visiting and news."""

set2 = "Hello world so that I can follow this now."

set3 = "lop lod lov love lore log lope london bridge is limp"

setCode = """
class Random36(random.Random):
    "Show the code included in the Python 3.6 version of the Random class"


    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        'Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        '
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


"""

with open("../corpus.txt", 'r', encoding='utf-8') as fp:
    set4 = fp.read()

gen = MarcovWordGenerator()
gen._train_on_text(set4)



generated = ""

for i in range(100):
    generated += gen.make_word() + " "

print(generated)

gen.saveModel('test.json')

