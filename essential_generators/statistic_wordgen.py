from essential_generators import Random36
import random

class StatisticTextGenerator():

    letters = "".join(
        ['a' * 81, 'b' * 14, 'c' * 27, 'd' * 42, 'e' * 127, 'f' * 22, 'g' * 20, 'h' * 60, 'i' * 69, 'j' * 1, 'k' * 7,
         'l' * 40, 'm' * 24, 'n' * 67, 'o' * 75, 'p' * 19, 'r' * 59, 's' * 63, 't' * 90, 'u' * 27, 'v' * 9, 'w' * 23,
         'x', 'y' * 19, 'z'])
    # word lengths up to 9
    word_lens = [1]*3 + [2]*18 + [3]*20 + [4]*15 + [5]*10 + [7]*8 + [8]*6 + [9]*4
    bigrams = ['th'] * 35 + ['he'] * 30 + ['in'] * 24 + ['er'] * 20 + ['an'] * 19 + ['re'] * 18 + ['on'] * 17
    bigrams += ['at'] * 14 + ['en'] * 14 + ['nd'] * 13 + ['ti'] * 13 + ['es'] * 13 + ['es'] * 12 + ['or'] * 12
    bigrams += ['te'] * 12 + ['ed'] * 11 + ['is'] * 11 + ['it'] * 11 + ['al'] * 10 + ['ar'] * 10 + ['st'] * 10

    def __init__(self):
        pass

    def gen_text(self, max_len=500):
        words = []

        for i in range(random.randint(1, max_len)):
            words.append(self.gen_word())

        return " ".join(words)

    def gen_word(self):
        """
        Generate a new word, based VERY loosely on

            letter frequencies here: https://en.wikipedia.org/wiki/Letter_frequency
            bigram frequencies here: #http://norvig.com/mayzner.html
        """

        word = ""
        word_len = random.choice(StatisticTextGenerator.word_lens)

        while len(word) < word_len:
            junction = random.random()
            if junction < .60:
                word += random.choice(StatisticTextGenerator.bigrams)
            elif junction < .80:
                word += random.choice(StatisticTextGenerator.letters) + random.choice(StatisticTextGenerator.letters)
            else:
                word += random.choice(StatisticTextGenerator.letters)

        return word



