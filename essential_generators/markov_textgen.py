import random
import os


class MarkovTextGenerator():

    startword = "STARTWORD"
    stopword = "STOPWORD"

    def __init__(self, model=None, load_model=True):
        self.grams = {}
        self.chain = {}
        if model is None:
            model_path = os.path.join(os.path.dirname(__file__), 'markov_textgen.json')
        else:
            model_path = model

        if load_model:
            self.load_model(model_path)
            self.chain_list = list(self.chain)

    def gen_word(self, safe_text=False):

        return random.choice(self.chain_list).split()[0]

    def gen_text(self, max_len=500):
        text = random.choice(self.chain_list).split()

        current_bigram = text[0]

        text_append = text.append
        space_join = " ".join
        while len(text) < max_len:
            transition = self._get_weighted_transition(current_bigram)
            if transition is not None:
                text_append(transition)
                current_bigram = space_join([text[-2], text[-1]])
            else:
                current_bigram = random.choice(self.chain_list)
                text += [self.chain[current_bigram]['left'], self.chain[current_bigram]['right']]

        response = " ".join(text).replace("<br/>", "\n")
        return response

    def _get_weighted_transition(self, bigram):
        if bigram not in self.chain:
            return None
        try:
            res = random.choices(self.chain[bigram]['transitions'], weights=self.chain[bigram]['weights'])
        except:
            return None

        if len(res) > 0:
            return res[0]

        return None

    def _condition_grams(self):
        bigram_transitions = {}

        for a, b, c in self.grams:

            bigram = "%s %s" % (a, b)
            trans_to = "%s" % (c)

            # print( "%s %s->%s %i" % (a,b,c, self.grams[(a,b,c,)]) )

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
            # also, while we are here..
            words = bigram.split()
            bigram_transitions[bigram]['left'] = words[0]
            bigram_transitions[bigram]['right'] = words[1]

        self.chain = bigram_transitions

        # print(bigram_transitions['+'])

    def _train_on_text(self, text):
        n = 3
        self.grams = {}
        gram_buffer = []
        lines = text.splitlines(keepends=False)

        for line in lines:
            words = line.split()

            if len(words) == 0:
                words = ["<br/>"]

            # words.append("<br/>")
            for word in words:
                # letter = letter.lower()
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

    def save_model(self, filepath):
        import json
        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(self.chain, fp, ensure_ascii=False)

    def load_model(self, filepath):
        import json
        with open(filepath, 'r', encoding='utf-8') as fp:
            self.chain = json.load(fp)

def run_it():
    gen = MarkovTextGenerator()
    for i in range(500):
        #print(i)
        text = gen.gen_text(10)

        #print(text)

if __name__ == '__main__':
    run_it()