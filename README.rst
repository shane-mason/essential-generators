Essential Document Generator
=============================

Dead Simple Document Generation
-------------------------------

Whether it's testing database performance or a new web interface, we've all needed a dead simple 
solution that'a flexible enough to generate a complex data set. If this is one of those times, 
you've come to the right place.

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
    'andease@tadn.tv'
    
    >>> gen.url()
    'https://atad.com/enasce.jsp'
    
    >>> gen.phone()
    '547-922-3848'
    
    >>> gen.slug()
    'ehillote-henaiour-ebemaice-qsiat76-heheellti'
    
    >>> gen.word()
    'enhihee'
    
    >>> gen.sentence()
    'hao orecoed menrial reis onheinete anyiicerth loi'
    
    >>> gen.paragraph()
    'Anliofea esrnema keriteceuofci hede urtooou andine thmaoor 
    haaresipino. Ngli oanndlaer erth qoreeyaomfu hewoleoraoein. 
    Onma ansieo icorof eteatsihng riemeuri ta iteoftorte onseclohe 
    hiano needmi. Chtoetete isdorokeou urtieconu allere ashaou 
    bel netthtooen ohaaktnatu erteaaero nguiaes eeso aall.'
        
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
        documents = gen.gen_docs(1000)

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
    gen.init_word_cache(5000)

In the first line, 5000 words are generated. In the second line, 5000 sentences made up of 5 to 
15 words from the word cache will be generated. subsequent call to `gen.word()` and `gen.sentence()`
will be selected from the caches. If you want to generate a new to a word or sentence not in the 
cache, call `gen.gen_word()` and `gen.gen_sentence()` respectively. If you want finer grain control,
`gen.word_cache` and `gen.sentence_cache` are arrays of strings that can be directly manipulated.

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

Disclaimer
-----------

The purpose of this module is to quickly generate data for use cases like load testing and 
performance evaluations. It attempts to mimic real data, but will not have the frequency or
statistical qualities of real world data. There are no warranties and this shouldn't 
be used for scientific, health or industrial purposes and so on...

Note that words are randomly generated (very loosely) based on character and bi-gram frequencies
found in the english language. Its a start, but beware that there's no sanitation, so its entirely 
very possible that real words and even phrases are generated - and this could include
objectionable content.

Why did I build this?
-----------------------

There are several great python module out there that generate fake data, so why did I make this?
Two reasons really:

1. I wanted a dead simple way to generate data to test other projects and I just wasn't finding
the flexibility I was looking for.
2. One of my problems with the existing approaches was the limited number of 'lorem ipsum' style words
that were available to generate text. I wanted to build a better lorem ipsum generator and this
made a nice platform.
