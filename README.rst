Essential Document Generator
=============================

Dead Simple Document Generation
-------------------------------

Whether it's testing database performance or a new web interface, we've all needed a dead simple
solution that'a flexible enough to generate a complex data set. If this is one of those times,
you've come to the right place. Essential Generators uses Markov chains to generate 'realistic' data -
and you can train them on your own data to make it even more real.

Install
~~~~~~~~

Using pip::

    pip install essential_generators


Use case: Get some random values
---------------------------------
Simple interface::

    >>> from essential_generators import DocumentGenerator

    >>> gen = DocumentGenerator()

    >>> gen.email()
    'cal.atis@prand.com'

    >>> gen.url()
    ''https://ver.co.uk/has/pron/sing/th.ablica-attrob79'

    >>> gen.phone()
    '547-922-3848'

    >>> gen.slug()
    'ehillote-henaiour-ebemaice-qsiat76-heheellti'

    >>> gen.word()
    'choleg'

    >>> gen.sentence()
    'Possess something historic and prehistoric sites within the family.'

    >>> gen.paragraph()
    "Country's total that roll clouds of gas that can affect. Officers: lieutenant aquifer system under
    the alaska supreme court, 14. About reality. perfect. this means that logic programs combine declarative
    and procedural law. some. 20.3% of other nations. during the meiji constitution, and assembled the imperial
    estates. Reduce visibility work during the regime withdrew from the crow in. Divert recyclable at 100.
    Applications. because no carbon, then all of which glucose (c6h12o6) and stearin (c57h110o6) are convenient.
    In french. forms can each be divided into: information theory. Therapeutic orientation. around haines. steven
    seagal's 1994 on deadly ground, starring michael caine.. Lakes and economic assistance (comecon). the states
    and 72 dependent. D.f.: comisión campaign tracking, allowing the companies running these. Were struggling moon
    io is volcanically active, and as the legal basis of chemical complexes.'

Use case: Make lots of complex documents
----------------------------------------

Let's say we are building a database for a new social media site. We have a preliminary schema and
want to test the server with some examples like this::


    {
        id: 39f96ef8-08e0-408e-b727-984372a95d9d,
        status: online,
        age: 27,
        homepage: johndoe.github.io,
        name: John Doe,
        headline: A Really Cool Guy
        about: Some longer profile text. Several Sentences.
    }

Document Templates
~~~~~~~~~~~~~~~~~~

Now let's say we want to generate hundreds of thousands of these records. For making documents,
we first need to define the template::

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
        documents = gen.documents(1000)

The template gives the structure and type for each field in the document. Note that `status` has
a list and not a single type; when a list is provided as the type, one of the items in the list
will be randomly selected for each generated documents using `random.choice(list)`

Custom Fields
~~~~~~~~~~~~~

Now we want to implement a new feature where users can rate each other between 1-5 stars and we want
to keep track of the average rating (a float between 1 and 5). We can do this by passing in a
function as the type, like so::

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
        'rating': gen_rating,
    }


In this case, when each document is created, `gen_rating` is called and the returned value is
added to the document.

Nested Documents
~~~~~~~~~~~~~~~~

Now that users are rating each other, of course they'll want to get in contact with each other.
The schema gets extended to include a nested `contact` object. Just like any custom field, we can
generate nested documents using generator functions as the type::

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


Word & Sentence Caching
~~~~~~~~~~~~~~~~~~~~~~~

Creating word and sentence cache's serves two purposes: it resticts the possible space of generated
elements to a discreet size (for instance, the average American's vocabulary is between 5k and 10k
words) and it greatly speeds subsequent document generation. Use them like this::

    gen.init_word_cache(5000)
    gen.init_sentence_cache(5000)

In the first line, 5000 words are generated. In the second line, 5000 sentences made up of 5 to
15 words from the word cache will be generated. subsequent call to `gen.word()` and `gen.sentence()`
will be selected from the caches. If you want to generate a new to a word or sentence not in the
cache, call `gen.gen_word()` and `gen.gen_sentence()` respectively. If you want finer grain control,
`gen.word_cache` and `gen.sentence_cache` are arrays of strings that can be directly manipulated.

Unique Fields
~~~~~~~~~~~~~
In this case, we want to gaurantee that the fields are unique. You can accomplish this by choosing 'guid'
as the field types, but that isn't good enough if you want the field to still look like an email address or a number. For
this case, we introduce the unique field::

    template = {
        'id': 'guid',
        'status': ['online', 'offline', 'dnd', 'anonymous'],
        'age': 'small_int',
        'homepage': 'url',
        'name': 'name',
        'headline': 'sentence',
        'about': 'paragraph',
        'primary_email': {'typemap': 'email', 'unique': True, 'tries': 10}
    }


In the primary_email field above, we passed a dictionary with the following pairs::

    typemap - what field type to generate (in this case 'email')
    unique - tells the generator that each value should be unique
    tries - the number of times that gen.email() will be called to try and get a unique entry. If a unique item can not
    generated in _tries_ iterations, the same number of iterations will be tried by generating a value and then adding
    1-5 random chars appended. If a unique value still isn't generated, then GUIDs are generated until a unique one is
    found.

The generator does its honest best to try and honor the type sent, but it prioritizes uniqueness. The default number of
tries is 10, so from our example above::

    10 attempts with 'generator.email()'
    10 attempts with 'generator.email() + generator.gen_chars()'
    infinite attempts with generator.guid()


Finer Grained Control
~~~~~~~~~~~~~~~~~~~~~

Now we want the user to be able to set a link to their current favorite post. You could do this
by adding a field called 'favpost' and settings its type to 'slug' (like the ones used to url-encode
blog post ids while keeping them human readable). The problem is, this would likely generate a
unique favpost for each document, but in the real world there would be a finite set of posts.

You can control this behaviour by using python lists as the type. In this example, we use a list
comprehension to generate a list of 1000 slugs that will be randomly seletected from when the documents
are generated::

    template = {
        'id': 'guid',
        'status': ['online', 'offline', 'dnd', 'anonymous'],
        'age': 'small_int',
        'homepage': 'url',
        'name': 'name',
        'headline': 'sentence',
        'about': 'paragraph',
        'favpost': [gen.slug() for n in range(1000)]
    }





So, what did we end up with?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is one result::

    {
        'name': 'Ster Ev',
        'age': 87,
        'status': 'anonymous',
        'favpost': 'anre-regtehcie57',
        'headline': 'ilrendna anr mo inttuonth anuir',
        'homepage': 'http://enar692.com/ten/erst/eresnn.heotiatin-neworwnti54-atnd',
        'id': 'ced10e96-b02c-4292-9be8-22dd8772c64e',
        'rating': 1.9779484996288086,
        'contact': {
                       'email': 'osat@ind.ru',
                       'phone': '695-323-8276'
                   }
        'about': 'Yeormftd or an on authar hei po heheat este ler hearain hethe
        hetiarte ti oren. Oncs yemf edhe inhe th bain thfin nanfee st. Thheannd
        chenes hein thin. Edrdth ttind te uearedor heoea hehaeren seonstth tith
        vemoal an rein gel don in. Anao is fecttrr.',

    }

Documents are basic Python dictionaries, so you can use the directly in your program or convert
them to json or any other serialization format for testing anywhere.

Word and Text Generation
-------------------------

Essential generators come with 3 builtin word and text generators:

**MarkovTextGenerator**
This approach uses a Markov chain to generate text. In this case, the generator is trained on text
to generate somewhat realistic random text from real words.

**MarkovWordGenerator**
This approach uses a Markov chain to generate words. In this case, the generator is trained on text
to generate somewhat realistic random words based on observed words.

**StatisticTextGenerator**
This approach uses statistical distributions to generate words that are similar to real words.

MarkovTextGenerator
~~~~~~~~~~~~~~~~~~~~
**MarkovTextGenerator** generates random text from real words using word level bigram frequency. This is the default for generating
sentences and paragraphs.

Example Word::

    fifteen

Example Text::

    reports the its citizens holding a tertiary education degree. Although Japan has 19 World Heritage List, fifteen of which
    track the same species, several intermediate stages occur between sea and to a professional social network analysis,
    network science, sociology, ethnography, statistics, optimization, and mathematics. The Vega Science Trust – science
    videos, including physics Video: Physics "Lightning" Tour with Justin Morgan 52-part video course...


MarkovWordGenenerator
~~~~~~~~~~~~~~~~~~~~~~
**MarkovWordGenenerator** generates random words from real letters using letter level bigram frequency. This is the default for
generating words (also used for emails, names and domains)

Example Word::

    groboo

Example Text::

    Remes way by entrun co. Forche 40-194 quilim The lace colost thigag toures loples opprou Alpite go. of andian It Afte
    imps stions revain Goto Stedes remapp go coutle Sountl doingu ablech thed al in whiclu thican Ocepro In havelo var clowne
    the of couthe...

StatisticWordGenerator
~~~~~~~~~~~~~~~~~~~~~~
**StatisticWordGenerator** generates random words from statistical distributions observed in a large corpus.

Example Word::

    anamer

Example Text::

    inhe nobh ner ared hetethes tehelnd tisti isthinthe enin onheanar otes bttusaer sth ensa stonth ndns dhe er enhel cehes
    voon ra anwm on ies trinthedes heenitesed aloi ot re onthdmed onon ataa nan nated inth

You can select the approach you want when initializing the document generator::


    #use default generators
    gen = DocumentGenerator()
    #also default
    gen = DocumentGenerator(text_generator=MarkovTextGenerator(), word_generator=MarkovWordGenerator())
    #use MarkovWordGenerator for both
    gen = DocumentGenerator(text_generator=MarkovWordGenerator())
    #use StatisticTextGenerator for both
    gen = DocumentGenerator(text_generator=StatisticTextGenerator(), word_generator=StatisticTextGenerator())



Creating New Models
-------------------

Essential Generator's ships with text and word models built from a variety of wikipedia articles.
There are three scripts included to help you generate new models:

build_corpus.py - Retrieves specified articles from wikipedia to use when training the models. Default output is
'corpus.txt'.
build_text_model.py - Uses corpus.txt to output markov_textgen.json as the text model for sentences and paragraphs.
build_word_model.py - Uses corpus.txt to output markov_wordgen.json as the word model (for words, email, domains etc)

Disclaimer
-----------

The purpose of this module is to quickly generate data for use cases like load testing and
performance evaluations. It attempts to mimic real data, but will not have the frequency or
statistical qualities of real world data. There are no warranties and this shouldn't
be used for scientific, health or industrial purposes and so on...


Why did I build this?
-----------------------

There are several great python module out there that generate fake data, so why did I make this?
Two reasons really:

1. I wanted a dead simple way to generate data to test other projects and I just wasn't finding
the flexibility I was looking for.
2. One of my problems with the existing approaches was the limited number of 'lorem ipsum' style words
that were available to generate text. I wanted to build a better lorem ipsum generator and this
made a nice platform.
