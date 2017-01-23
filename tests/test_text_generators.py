import unittest
from essential_generators import MarcovTextGenerator, MarcovWordGenerator, StatisticTextGenerator
import random


class TestMarkovTextGenerator(unittest.TestCase):

    def test_markov_text(self):
        text = MarcovTextGenerator().gen_text()
        print("-TestMarkovTextGenerator.text"*5)
        print(text)

    def test_markov_word(self):
        text = MarcovTextGenerator().gen_word()
        print("-TestMarkovTextGenerator.word" * 5)
        print(text)


class TestMarkovWordGenerator(unittest.TestCase):

    def test_markov_text(self):
        text = MarcovWordGenerator().gen_text()
        print("-TestMarkovWordGenerator.text" * 5)
        print(text)

    def test_markov_word(self):
        text = MarcovWordGenerator().gen_word()
        print("-TestMarkovWordGenerator.word" * 5)
        print(text)


class TestStatisticWordGenerator(unittest.TestCase):
    def test_statistic_text(self):
        text = StatisticTextGenerator().gen_text()
        print("TestStatisticWordGenerator.text-" * 5)
        print(text)

    def test_statistic_word(self):
        text = StatisticTextGenerator().gen_word()
        print("TestStatisticWordGenerator.word-" * 5)
        print(text)
