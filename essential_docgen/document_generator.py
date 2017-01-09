import random
import uuid
import sys


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
        self.index = 0
        self.fields = {}
        self.word_cache = []
        self.sentence_cache = []

    def init_word_cache(self, length=10000):
        """Create a words cache to speed up generation and to limit the number of possible words."""
        for i in range(0, length):
            self.word_cache.append(self.gen_word())

    def init_sentence_cache(self, length=10000):
        """Create a words cache to speed up generation and to limit the number of possible words."""
        for i in range(0, length):
            self.sentence_cache.append(self.gen_sentence())

    def word(self):
        """Gets a word from the words cache or generates a new word if the cache is empty"""
        if len(self.word_cache) > 0:
            return random.choice(self.word_cache)
        else:
            return self.gen_word()

    def sentence(self):
        """Gets a sentence from the word cache or generates a new word if the cache is empty"""
        if len(self.sentence_cache) > 0:
            return random.choice(self.sentence_cache)
        else:
            return self.gen_sentence()

    def gen_word(self):
        """
        Generate a new word, based VERY loosely on

            letter frequencies here: https://en.wikipedia.org/wiki/Letter_frequency
            bigram frequencies here: #http://norvig.com/mayzner.html
        """

        word = ""
        word_len = random.choice(DocumentGenerator.word_lens)

        while len(word) < word_len:
            junction = random.random()
            if junction < .60:
                word += random.choice(DocumentGenerator.bigrams)
            elif junction < .80:
                word += random.choice(DocumentGenerator.letters) + random.choice(DocumentGenerator.letters)
            else:
                word += random.choice(DocumentGenerator.letters)

        return word

    def gen_sentence(self, min_words=3, max_words=15):
        """Generate a new sentence - will use cached words if existing."""
        sentence = ""
        for i in range(random.randint(min_words, max_words)):
            sentence += self.word() + " "
        return sentence.strip()

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
            domain = "%s.%s" % (self.gen_word(), random.choice(tld))
        elif junction < .9:
            domain = "%s.%s.%s" % (self.gen_word(), self.gen_word(), random.choice(tld))
        else:
            domain = "%s%i.%s" % (self.gen_word(), random.randint(1, 999), random.choice(tld))
        return domain

    def email(self):
        """Generate a new email address."""
        email = ""
        junction = random.random()
        domain = self.domain()

        if junction < .75:
            email = "%s@%s" % (self.gen_word(), self.domain())
        elif junction < .9:
            email = "%s.%s@%s" % (self.gen_word(), self.gen_word(), self.domain())
        else:
            email = "%s%i@%s" % (self.gen_word(), random.randint(1, 999), self.domain())

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
            url += "/%s" % self.gen_word()

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
                slug += "-" + self.gen_word()
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
        return "%s %s" % (self.word().capitalize(), self.word().capitalize())

    def document(self):
        """Generate a document based on the current template"""
        doc = {}
        type_map = {
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

        for field in self.template:
            if isinstance(self.template[field], list):
                doc[field] = random.choice(self.template[field])
            elif self.template[field] in type_map:
                doc[field] = type_map[self.template[field]]()
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
