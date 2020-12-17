import os
import random

class MarkovWordGenerator():
    startword = "STARTWORD"
    stopword = "STOPWORD"

    def __init__(self, model=None, load_model=True):
        self.grams = {}
        self.chain = {}

        if model is None:
            model_path = os.path.join(os.path.dirname(__file__) + '/markov_wordgen.json')
        else:
            model_path = model

        if load_model:
            self.load_model(model_path)

    def gen_word(self, max_len=15):
        word = MarkovWordGenerator.startword
        current_bigram = MarkovWordGenerator.startword
        while len(word) < max_len:
            transition = self._get_weighted_transition(current_bigram)

            if transition is not None:
                word += transition
                current_bigram = word[-2:]
            else:
                break

        return word.replace(MarkovWordGenerator.startword, "").replace(MarkovWordGenerator.stopword, "")

    def gen_text(self, max_len=500):

        words = []

        for i in range(1, random.randint(0, max_len)):
            words.append(self.gen_word())

        return " ".join(words)

    def _get_weighted_transition(self, bigram):
        if bigram not in self.chain:
            return None
        
        res = random.choices(self.chain[bigram]['transitions'], weights=self.chain[bigram]['weights'])
        if len(res) > 0:
            return res[0]

        return None

    def _condition_grams(self):
        bigram_transitions = {}
        for a, b, c in self.grams:

            if a == MarkovWordGenerator.startword:
                # not really a bigram in this case
                bigram = "%s" % (a)
                trans_to = "%s%s" % (b, c)

            else:
                bigram = "%s%s" % (a, b)
                trans_to = "%s" % (c)

            # print( "%s%s->%s %i" % (a,b,c, self.grams[(a,b,c,)]) )

            if bigram not in bigram_transitions:
                bigram_transitions[bigram] = {}
            if c not in bigram_transitions[bigram]:
                bigram_transitions[bigram][trans_to] = 0
            if 'total' not in bigram_transitions[bigram]:
                bigram_transitions[bigram]['total'] = 0

            bigram_transitions[bigram]['total'] += self.grams[(a, b, c,)]
            bigram_transitions[bigram][trans_to] += self.grams[(a, b, c,)]

        # now, get the percentages for each
        for bigram in bigram_transitions:
            weights = []
            transitions = []
            for trans in bigram_transitions[bigram]:
                if trans != 'total':
                    percent = bigram_transitions[bigram][trans] / bigram_transitions[bigram]['total']
                    bigram_transitions[bigram][trans] = percent

                    weights.append(percent)
                    transitions.append(trans)

            bigram_transitions[bigram]['weights'] = weights
            bigram_transitions[bigram]['transitions'] = transitions

        self.chain = bigram_transitions

        # print(bigram_transitions['+'])

    def _train_on_text(self, text):
        n = 3
        self.grams = {}
        gram_buffer = []

        for letter in text:
            # letter = letter.lower()

            if letter not in ['\n', ' ']:
                gram_buffer.append(letter)
            else:
                gram_buffer.append(MarkovWordGenerator.stopword)

            if len(gram_buffer) >= n:
                as_tuple = tuple(gram_buffer)
                if as_tuple not in self.grams:
                    self.grams[as_tuple] = 0

                self.grams[as_tuple] += 1

                gram_buffer = gram_buffer[1:]

            if letter in ['\n', ' ', '*']:
                gram_buffer.clear()
                gram_buffer.append(MarkovWordGenerator.startword)

    def train(self, text):
        self._train_on_text(text)
        self._condition_grams()

    def save_model(self, filepath):
        import json
        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(self.chain, fp, ensure_ascii=False)

    def load_model(self, filepath):
        import json
        with open(filepath, 'r', encoding='utf-8') as fp:
            self.chain = json.load(fp)


