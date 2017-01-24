from essential_generators import MarcovWordGenerator

def make_training_data(corpus="corpus.txt", output="../essential_generators/markov_wordgen.json"):
    with open(corpus, 'r', encoding='utf-8') as fp:
        set4 = fp.read()

    gen = MarcovWordGenerator(load_model=False)
    gen.train(set4)
    gen.save_model(output)


make_training_data()
