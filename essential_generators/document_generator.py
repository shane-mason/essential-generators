import random
import uuid
import sys
from essential_generators import MarkovWordGenerator, MarkovTextGenerator, StatisticTextGenerator
import re
import string

class DocumentGenerator:
    """
    Fake document generator::

        def nested_item():
            nested_gen = DocumentGenerator()
            nested_gen.set_template({'user': 'email', 'hash': 'gid', 'posts': small_int})
            return nested_gen.gen_doc()

        generator = DocumentGenerator()
        generator.set_template({'id': 'index', 'user': nested_item, 'url': 'url', 'age': 43, 'one_of': ['male', 'female', 'both']})
        print(generator.gen_docs(5))

        Word generation based VERY loosely on

            letter frequencies here: https://en.wikipedia.org/wiki/Letter_frequency
            bigram frequencies here: #http://norvig.com/mayzner.html

    """

    def __init__(self, word_generator=None, text_generator=None, type_map={}):
        self.index = 0
        self.fields = {}
        self.word_cache = []
        self.sentence_cache = []
        self.unique_cache = {}


        if word_generator is None:
            self.word_generator = MarkovWordGenerator()
        else:
            self.word_generator = word_generator

        if text_generator is None:
            self.text_generator = MarkovTextGenerator()
        else:
            self.text_generator = text_generator

        self.type_map = {
            'index': self.index,
            'word': self.gen_word,
            'sentence': self.gen_sentence,
            'paragraph': self.paragraph,
            'email': self.email,
            'guid': self.guid,
            'url': self.url,
            'small_int': self.small_int,
            'integer': self.integer,
            'small_float': self.small_float,
            'floating': self.floating,
            'upc': self.upc,
            'name': self.name,
            'slug': self.slug

        }

        if type_map is not None:
            self.type_map.update(type_map)

    def init_word_cache(self, length=10000):
        """Create a words cache to speed up generation and to limit the number of possible words."""
        for i in range(0, length):
            self.word_cache.append(self.gen_word())

    def init_sentence_cache(self, length=10000):
        """Create a words cache to speed up generation and to limit the number of possible words."""
        for i in range(0, length):
            #print(i)
            self.sentence_cache.append(self.gen_sentence())

    def word(self, safe_word=False):
        """Gets a word from the words cache or generates a new word if the cache is empty"""
        word = None

        while word == None:
            if len(self.word_cache) > 0:
                word = random.choice(self.word_cache)
            else:
                word = self.gen_word()

            if safe_word and re.search(r'\W', word) is not None:
                word = None

        return word


    def sentence(self):
        """Gets a sentence from the word cache or generates a new word if the cache is empty"""
        if len(self.sentence_cache) > 0:
            return random.choice(self.sentence_cache)
        else:
            return self.gen_sentence()


    def gen_chars(self, min=1, max=5):
        population = string.printable
        charlist = [random.choice(population) for i in range(min, max)]
        return "".join(charlist)

    def gen_word(self, safe_word=True):
        word = self.word_generator.gen_word()
        return word

    def gen_sentence(self, min_words=3, max_words=15):
        """Generate a new sentence - will use cached words if existing."""
        sentence = self.text_generator.gen_text(random.randint(min_words, max_words))
        sentence = sentence[0].upper() + sentence[1:]
        sentence = sentence.strip()

        ending = "."
        if random.random() > .95:
            ending = '?'
        elif random.random() > .98:
            ending = '!'

        sentence = re.sub(r'\W+$', ending, sentence)
        return sentence

    def paragraph(self, min_sentences=2, max_sentences=15):
        """Generate a new paragraph - will use cached sentences if existing."""
        paragraph = ""
        for i in range(random.randint(min_sentences, max_sentences)):
            paragraph += self.sentence().capitalize() + ". "

        return paragraph.strip()

    def domain(self):
        """Generate a new domain name."""
        domain = ""
        # https://w3techs.com/technologies/overview/top_level_domain/all
        tld = ['com', 'com', 'com', 'com', 'com', 'org', 'gov', 'biz', 'net', 'tv', 'us', 'edu', 'ru', 'co.uk', 'fr',
               'jp']

        junction = random.random()

        if junction < .75:
            domain = "%s.%s" % (self.word(True), random.choice(tld))
        elif junction < .9:
            domain = "%s.%s.%s" % (self.word(True), self.word(True), random.choice(tld))
        else:
            domain = "%s%i.%s" % (self.word(True), random.randint(1, 999), random.choice(tld))
        return domain

    def email(self):
        """Generate a new email address."""
        email = ""
        junction = random.random()
        domain = self.domain()

        if junction < .75:
            email = "%s@%s" % (self.word(True), self.domain())
        elif junction < .9:
            email = "%s.%s@%s" % (self.word(True), self.word(True), self.domain())
        else:
            email = "%s%i@%s" % (self.word(True), random.randint(1, 999), self.domain())

        return email

    def phone(self):
        """Generate a new email address."""
        return "%i-%i-%s" % (random.randint(200, 999), random.randint(111, 999), str(random.randint(0, 9999)).zfill(4))

    def guid(self):
        """Genrate a new GUID - based on uuid.uuid4"""
        return str(uuid.uuid4())

    def set_template(self, template):
        """Set the template for document generation."""
        self.template = template

    def index(self):
        """Get the next number in the index."""
        self.index += 1
        return self.index

    def url(self):
        """Genrate a new URL"""
        mimes = ['html', 'html', 'html', 'html', 'asp', 'jsp', 'php', 'png', 'jpg', 'gif']
        junction = random.random()
        url = self.domain()

        proto = "http"
        if random.random() < .50:
            proto = "https"

        url = "%s://%s" % (proto, url)

        path_depth = random.randint(0, 4)
        for i in range(path_depth):
            url += "/%s" % self.word(True)

        ending = random.random()
        if ending < .30:
            url = "%s.%s" % (url, random.choice(mimes))
        elif ending < 60:
            url = "%s.%s" % (url, self.slug())

        return url

    def slug(self):
        slug = self.word()
        for i in range(random.randint(2, 6)):
            if (random.random() < .8):
                slug += "-" + self.word(True)
            else:
                slug += str(self.small_int())
        return slug

    def small_int(self):
        """Generate an int between 0 and 99"""
        return random.randint(0, 99)

    def integer(self):
        """Generate an int between 0 and sys.maxsize"""
        return random.randint(0, sys.maxsize)

    def small_float(self):
        """Generate a float between 0 and 1"""
        return random.random()

    def floating(self):
        """Generate an float between 0 and sys.maxsize"""
        return random.random() * sys.maxsize

    def upc(self):
        upc = ""
        for i in range(0, 12):
            upc += str(random.randint(0, 9))
        return upc

    def name(self):
        return "%s %s" % (self.word(True).capitalize(), self.word(True).capitalize())


    def _find_unique(self):
        pass

    def document(self):
        """Generate a document based on the current template"""
        doc = {}

        for field in self.template:
            if isinstance(self.template[field], list):
                doc[field] = random.choice(self.template[field])
            elif isinstance(self.template[field], dict):
                if 'unique' in self.template[field]:
                    if self.template[field]['unique']:
                        found_unique = False
                        if field not in self.unique_cache:
                            self.unique_cache[field] = {}

                        max_tries = 0
                        if 'tries' in self.template[field]:
                            max_tries = self.template[field]['tries']

                        tries = 0
                        while not found_unique:
                            if tries < max_tries:
                                val = self.type_map[self.template[field]['typemap']]()
                            elif tries < max_tries*2:
                                val = self.type_map[self.template[field]['typemap']]() + self.gen_chars()
                            else:
                                val = self.guid()

                            if val not in self.unique_cache[field]:
                                self.unique_cache[field][val] = True
                                found_unique = True

                            tries += 1

                    else:
                        doc[field] = self.type_map[self.template[field]['typemap']]()

            elif self.template[field] in self.type_map:
                doc[field] = self.type_map[self.template[field]]()
            elif callable(self.template[field]):
                doc[field] = self.template[field]()
            else:
                doc[field] = self.template[field]
        return doc

    def documents(self, count):
        """Generate an list of documents"""
        docs = []
        for i in range(count):
            docs.append(self.document())

        return docs



#gen = DocumentGenerator(text_generator=MarkovTextGenerator(), word_generator=MarkovWordGenerator)