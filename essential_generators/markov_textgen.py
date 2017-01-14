from essential_generators import Random36
import random

class MarcovWordGenerator():
    startword = "%"
    stopword = "%"

    def __init__(self):
        self.grams = {}
        self.chain = {}


    def make_text(self, max_len=500, bigram_start=None):

        if bigram_start is not None:
            text = bigram_start.split()
        else:
            text = random.choice(list(self.chain)).split()

        current_bigram = text[0]
        #print("Here:",current_bigram)

        while len(text) < max_len:
            transition = self._get_weighted_transition(current_bigram)
            if transition != None:
                text.append(transition)
                current_bigram = "%s %s" % (text[-2], text[-1])
                #print("Current:", current_bigram)

            else:

                text.append("\n")
                transition = random.choice(list(self.chain))
                current_bigram = random.choice(list(self.chain))
                words = current_bigram.split()
                text+=words



        return " ".join(text)


    def _get_weighted_transition(self, bigram):
        if bigram not in self.chain:
            return None
        try:
            res = Random36().choices(self.chain[bigram]['transitions'], weights=self.chain[bigram]['weights'])
        except:
            return None

        if len(res) > 0:
            return res[0]

        return None


    def _condition_grams(self):
        bigram_transitions = {}
        for a,b,c in self.grams:

            bigram = "%s %s" % (a, b)
            trans_to = "%s" % (c)

            print( "%s %s->%s %i" % (a,b,c, self.grams[(a,b,c,)]) )

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
        lines = text.splitlines(keepends=False)

        for line in lines:
            words = line.split()

            if len(words) == 0:
                word = "\n"

            for word in words:
                #letter = letter.lower()
                gram_buffer.append(word)

                if len(gram_buffer) >= n:
                    as_tuple = tuple(gram_buffer)
                    if as_tuple not in self.grams:
                        self.grams[as_tuple] = 0
                    self.grams[as_tuple] += 1


                    gram_buffer = gram_buffer[1:]


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



set1 = """“

And yet I meant to be uncommonly clever in taking so decided a dislike
to him, without any reason. It is such a spur to one’s genius, such an
opening for wit, to have a dislike of that kind. One may be continually
abusive without saying anything just; but one cannot always be laughing
at a man without now and then stumbling on something witty.”

“Lizzy, when you first read that letter, I am sure you could not treat
the matter as you do now.”

“Indeed, I could not. I was uncomfortable enough, I may say unhappy. And
with no one to speak to about what I felt, no Jane to comfort me and say
that I had not been so very weak and vain and nonsensical as I knew I
had! Oh! how I wanted you!”

“How unfortunate that you should have used such very strong expressions
in speaking of Wickham to Mr. Darcy, for now they do appear wholly
undeserved.”

"""

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

gen.train(set4)


generated = gen.make_text()

print("-"*25)
print(generated.replace("\n", "\n\n"))



gen.saveModel('test.json')

