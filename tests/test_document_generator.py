import unittest
from essential_generators import DocumentGenerator
import random


class TestDocumentGenerator(unittest.TestCase):

    def test_template(self):
        gen = DocumentGenerator()

        template = {
            'id': 'guid',
            'status': ['online', 'offline', 'dnd', 'anonymous'],
            'age': 'small_int',
            'homepage': 'url',
            'name': 'name',
            'headline': 'sentence',
            'about': 'paragraph'
        }

        gen.set_template(template)
        documents = gen.documents(10)
        self.assertEqual(len(documents), 10)

    def test_custom_field(self):
        gen = DocumentGenerator()

        def gen_rating():
            return random.uniform(1, 5)

        template = {
            'id': 'guid',
            'status': ['online', 'offline', 'dnd', 'anonymous'],
            'age': 'small_int',
            'homepage': 'url',
            'name': 'name',
            'headline': 'sentence',
            'about': 'paragraph',
            'rating': gen_rating
        }

        gen.set_template(template)
        documents = gen.documents(10)
        self.assertEqual(len(documents), 10)

    def test_nested_field(self):
        gen = DocumentGenerator()

        def gen_contact():
            return {
                'email': gen.email(),
                'phone': gen.phone()
            }

        template = {
            'id': 'guid',
            'status': ['online', 'offline', 'dnd', 'anonymous'],
            'age': 'small_int',
            'homepage': 'url',
            'name': 'name',
            'headline': 'sentence',
            'about': 'paragraph',
            'contact': gen_contact
        }

        gen.set_template(template)
        documents = gen.documents(10)
        self.assertEqual(len(documents), 10)

    def test_cache(self):
        gen = DocumentGenerator()
        gen.init_word_cache(5000)
        gen.init_sentence_cache(5000)


        self.assertEqual(len(gen.word_cache), 5000)
        self.assertEqual(len(gen.sentence_cache), 5000)

    def test_all(self):
        gen = DocumentGenerator()

        def gen_contact():
            return {
                'email': gen.email(),
                'phone': gen.phone()
            }

        def gen_rating():
            return random.uniform(1, 5)

        template = {
            'id': 'guid',
            'status': ['online', 'offline', 'dnd', 'anonymous'],
            'age': 'small_int',
            'homepage': 'url',
            'name': 'name',
            'headline': 'sentence',
            'about': 'paragraph',
            'email': { 'typemap': 'email', 'unique': True },
            'rating': gen_rating,
            'contact': gen_contact,
            'favpost': [gen.slug() for n in range(1000)]
        }

        gen.set_template(template)
        documents = gen.documents(10)
        print(documents[0])
        self.assertEqual(len(documents), 10)


